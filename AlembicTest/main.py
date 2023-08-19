import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models import User
from models.user import GenderType

async def main():
    engine = create_async_engine("sqlite+aiosqlite:///app.db", echo=True)

    SessionMaker = async_sessionmaker(engine, expire_on_commit=False)

    new_user = User(
        email='sammanan4@gmail.com',
        password='Test@123',
        gender=GenderType.male.value,
        date_of_birth=datetime.today().date()
    )
    async with SessionMaker() as session:
        session.add(new_user)
        await session.commit()
    
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()
asyncio.run(main())