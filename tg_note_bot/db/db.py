"""

"""

# session: AsyncSession

# async def main():
#     async with async_session() as session:
#         async with session.begin():
#             session.add_all(
#                 [
#                     Users(tg_id=10),
#                     Users(tg_id=20),
#                     Users(tg_id=30),
#                 ]
#             )
#
#     async with async_session() as session:
#         print('-------------------')
#         result = await session.execute(select(Users))
#         print(result.all())
#
#     async with async_session() as session:
#         session.add_all(
#             [
#                 Rubrics(name='Football', user_id=1),
#                 Rubrics(name='Box', user_id=2),
#                 Rubrics(name='Piano', user_id=1)
#             ]
#         )
#         await session.commit()
#
#     async with async_session() as session:
#         print('-------------------')
#         result = await session.execute(select(Users))
#         await session.run_sync([a.rubrics for a in result.scalars()])