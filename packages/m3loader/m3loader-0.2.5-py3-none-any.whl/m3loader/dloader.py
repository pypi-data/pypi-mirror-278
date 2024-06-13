import os
import asyncio
import aiohttp
from tqdm.asyncio import tqdm
import ffmpeg
import sys
import time
from urllib.parse import urljoin
import argparse
import shutil

def download(m3u8_url, output_path='.', output_name=None, progress=False, timeout=None, retries=None):
    """
    Downloads and merges M3U8 segments into a single MP4 file.

    Parameters:
    - m3u8_url (str): URL of the M3U8 file.
    - output_path (str): Output path for the MP4 file. Default is the current directory.
    - output_name (str): Output file name (with or without .mp4 extension). If not provided, a default name is used.
    - progress (bool): Show progress bar and merging messages. Default is False.
    - timeout (int): Set timeout for downloading in seconds. Default is None.
    - retries (int): Set maximum number of retries for downloading segments. Default is None.
    """

    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Determine output file name and path
    if output_name:
        if not output_name.endswith('.mp4'):
            output_name += '.mp4'
        output_file = os.path.join(output_path, output_name)
    else:
        output_file = os.path.join(output_path, f"m3Loader_{int(time.time())}.mp4")

    m3_name = output_file.replace('.mp4', '.m3u8')

    # Create a unique segments folder
    segments_path = os.path.join(output_path, f'segments_{int(time.time())}')
    os.makedirs(segments_path, exist_ok=True)

    # Function to download a segment asynchronously with retries
    async def download_segment(session, url, segment_name, retries=0, pbar=None):
        attempt = 0
        while attempt <= retries:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to download segment: {url}")
                    with open(segment_name, 'wb') as file:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)
                if pbar:
                    pbar.update(1)
                return
            except Exception:
                attempt += 1
                if attempt > retries:
                    raise

    # Read the M3U8 file to get the segment URLs
    async def download_m3u8():
        async with aiohttp.ClientSession() as session:
            async with session.get(m3u8_url) as response:
                m3u8_content = await response.text()
                with open(m3_name, 'w') as file:
                    file.write(m3u8_content)

    # Run the download_m3u8 function
    asyncio.run(download_m3u8())

    # Parse the M3U8 file
    with open(m3_name, 'r') as file:
        lines = file.readlines()

    segment_urls = [urljoin(m3u8_url, line.strip()) for line in lines if line and not line.startswith("#")]

    # Prepare segment names with the directory path
    segment_names = [os.path.join(segments_path, f'segment_{i:05d}.ts') for i in range(len(segment_urls))]

    # Main function to download segments and merge them
    async def main():
        # Download segments in parallel using aiohttp
        async def download_all_segments():
            async with aiohttp.ClientSession() as session:
                tasks = []
                retries_count = retries if retries else 0
                if progress:
                    with tqdm(total=len(segment_urls), desc="Downloading segments") as pbar:
                        for url, name in zip(segment_urls, segment_names):
                            task = download_segment(session, url, name, retries_count, pbar)
                            tasks.append(task)
                        await asyncio.gather(*tasks)
                else:
                    for url, name in zip(segment_urls, segment_names):
                        task = download_segment(session, url, name, retries_count)
                        tasks.append(task)
                    await asyncio.gather(*tasks)

        start_time = time.time()
        try:
            if timeout:
                await asyncio.wait_for(download_all_segments(), timeout=timeout)
            else:
                await download_all_segments()
        except (asyncio.TimeoutError, aiohttp.ClientPayloadError, aiohttp.http_exceptions.TransferEncodingError) as e:
            print(f"Error: {e}")
            cleanup()
            sys.exit(1)
        end_time = time.time()

        # Verify all segments are downloaded
        missing_segments = [segment for segment in segment_names if not os.path.exists(segment) or os.path.getsize(segment) == 0]
        if missing_segments:
            print(f"Missing or empty segments: {missing_segments}")
            cleanup()
            sys.exit(1)

        # List downloaded segments
        segments = sorted(segment_names)

        # Print merging message if progress flag is set
        if progress:
            print("Merging segments...")

        # Write segment file paths to a text file
        filelist_path = os.path.join(output_path, f"filelist_{int(time.time())}.txt")
        with open(filelist_path, "w") as filelist:
            for segment in segments:
                filelist.write(f"file '{os.path.abspath(segment)}'\n")

        # Combine the segments into an MP4 file using ffmpeg-python
        ffmpeg.input(filelist_path, format='concat', safe=0).output(output_file, c='copy').run(overwrite_output=True, quiet=True)

        # Calculate file size and download speed
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # Convert to MB
        total_time = end_time - start_time
        download_speed = file_size / total_time  # MB/s

        # Remove the segments and the M3U8 file
        for segment in segments:
            os.remove(segment)

        os.remove(m3_name)
        os.remove(filelist_path)

        # Clean the segments folder if empty
        shutil.rmtree(segments_path)

        print(f"Downloaded {output_file} {file_size:.2f} MB in {total_time:.2f} seconds | Speed: {download_speed:.2f} MB/s")

    def cleanup():
        """Clean up downloaded segments and temporary files."""
        if os.path.exists(segments_path):
            shutil.rmtree(segments_path)
        if os.path.exists(m3_name):
            os.remove(m3_name)

    # Run the main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Process interrupted. Cleaning up...")
        cleanup()
        sys.exit(1)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Download and merge M3U8 segments into an MP4 file.')
    parser.add_argument('m3u8_url', help='URL of the M3U8 file')
    parser.add_argument('-p', '--progress', action='store_true', help='Show progress bar and merging messages')
    parser.add_argument('-t', '--timeout', type=int, help='Set timeout for downloading in seconds')
    parser.add_argument('-r', '--retries', type=int, help='Set maximum number of retries for downloading segments')
    parser.add_argument('-d', '--output-path', default='.', help='Output path for the MP4 file')
    parser.add_argument('-o', '--output-name', help='Output file name (with or without .mp4 extension)')
    args = parser.parse_args()

    download(
        m3u8_url=args.m3u8_url,
        output_path=args.output_path,
        output_name=args.output_name,
        progress=args.progress,
        timeout=args.timeout,
        retries=args.retries
    )

if __name__ == '__main__':
    main()
