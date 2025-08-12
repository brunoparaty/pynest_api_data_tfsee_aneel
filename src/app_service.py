from nest.core import Injectable

@Injectable()
class AppService:
    
    def get_status(self) -> dict:
        return {"status": "ok", "message": "ANEEL Jobs API is running!"}