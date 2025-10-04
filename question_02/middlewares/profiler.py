import os
from fastapi import Request
from pyinstrument import Profiler



import os
from datetime import datetime
from pyinstrument import Profiler
from fastapi import Request
class ProfilerUtils:    
    @staticmethod
    def generate_profile_filename(endpoint_path: str, prefix: str = ""):
        """Generate structured filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        safe_endpoint = endpoint_path.strip("/").replace("/", "_")
        return f"{prefix}{timestamp}_{safe_endpoint}.html"

    @staticmethod
    def get_profile_directory():
        profile_dir = os.path.join(
            "profiles", 
            datetime.now().strftime("%Y-%m-%d")
        )
        os.makedirs(profile_dir, exist_ok=True)
        return profile_dir

    
async def profile_http_middleware(request: Request, call_next):

    profiler = Profiler()
    endpoint_path = request.url.path
    profiler.start()

    try:
        response = await call_next(request)
        return response
    finally:
        profiler.stop()
        
        filename = ProfilerUtils.generate_profile_filename(endpoint_path)
        profile_dir = ProfilerUtils.get_profile_directory()
        filepath = os.path.join(profile_dir, filename)
        with open(filepath, "w") as f:
            f.write(profiler.output_html())

