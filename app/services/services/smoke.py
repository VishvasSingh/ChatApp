

class SmokeService:

    @staticmethod
    async def get_version():
        metadata = {"app": "ChatApp", "version": "1.0"}
        return metadata

