from threading import Thread
import os
import requests
from tqdm import tqdm\
    
from .utils import *

class MultiThreadDownloader():
    """
    Multi thread downloader base class
    
    param:url - The URL of remote file
    param:chunk_size
    """
    def __init__(self, url, chunk_size: int = 1000000, filename: None | str = None):
        
        self.url = url
        self.chunk_size =chunk_size
        self.tell = 0
        if filename is None:
            filename = os.path.basename(self.url).split("?")[0]
            
        if os.path.exists(filename):
            keep = input(f"{os.path.abspath(filename)} already exists, overite it? [y/n] ")
            if keep.lower() == "y":
                pass
            elif keep.lower() == "n":
                abort_with_exception("Not to overwrite, aborting......", 17)
            else:
                raise FileExistsError("Can't understand operation, must in 'yYnN'.")
            
        self.out_file = open(filename, "wb")
        self.completed_thread_count = 0
        self.downloaded = 0
        
        def _get_content_length(url):
            res = requests.get(self.url, stream=True)
            #print(res.content)
            return int(res.headers["Content-Length"])
        self.content_length = _get_content_length(self.url)
        
        
        print(f"Downloading {self.url} as file {os.path.abspath(self.out_file.name)} ({self.content_length} bytes)")
        
        
        self.total_thread_count = (self.content_length // self.chunk_size) + 1
        self.placeholder = [None] * self.total_thread_count
        self.progress_bar = tqdm(unit='B', unit_scale=True, desc='Downloading', total=self.content_length)
        assert len(self.placeholder) == self.total_thread_count, "Two values aren't equal!"
        
    @abort_if_exception
    def _cget(self, hd):
        try:
            resp = requests.get(self.url, headers=hd, stream=True)
        except ConnectionError:
            return self._cget(hd=hd)
        return resp

    @abort_if_exception
    def get_chunk(self, start_offset: int, id_):
        end_offset = start_offset + self.chunk_size - 1
        if (end_offset+1) > self.content_length:
            end_offset = self.content_length
        #print(start_offset, end_offset)
        headers = {"Range": f"bytes={start_offset}-{end_offset}", "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
        response = self._cget(headers)
        content = response.content
        self.placeholder[id_] = content
        self.completed_thread_count += 1
        self.downloaded += len(content)
        self.progress_bar.update(len(content))
        return content
    
    @abort_if_exception
    def start(self):
        threads = []
        position = 0
        for i in range(0, self.total_thread_count):
            thread = Thread(target=self.get_chunk, args=[position, i])
            self.total_thread_count += 1
            threads.append(thread)
            position += self.chunk_size
            thread.start()
            
        for downloadThread in threads:
            downloadThread.join()
            
          
        self.progress_bar.close()
        print("Working on disk......")
        _ = 0
        while True:
            try:
                content = self.placeholder[_]
                self.out_file.write(content)
            except IndexError:
                break
            print_on_lastline(f"Chunk writted: {_+1}/{len(self.placeholder)}")
            _+=1
        
        print("\nDone.")
        #print(self.alldata.keys())
        self.kill()
            
    def kill(self):
        self.out_file.close()
        
    
if __name__ == "__main__":
    # test
    d = MultiThreadDownloader("https://github.com/BillLoic/unicode-table/releases/download/v1.0.0/unicode-table.zip.zip", 200000, "uct.zip")
    d.start()