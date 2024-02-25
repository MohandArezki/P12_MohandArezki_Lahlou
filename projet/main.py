import sentry_sdk
from console.main import Console
from controllers.database import DBManager

if __name__ == "__main__":
    try:
        sentry_sdk.init(
            dsn="https://ec243d4db509856d5d4454dc53d5e452@o4506676311949312.ingest.sentry.io/4506676315947008",
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
        
    except Exception as sentry_error:
        print(f"Error initializing Sentry: {sentry_error}")
    
    try:
        DBManager.init("production")
    except Exception as db_error:
        print(f"Error initializing database: {db_error}")
    else:
        console = Console()
        console.cmdloop()
