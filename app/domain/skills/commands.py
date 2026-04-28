#
#
# async def update_category_name_command(
#     repository: RepositoryProtocol,
#     /,
#     data: SkillsCategoryUpdate,
# ) -> UpdateResult:
#     category = await repository.get_category(category_id=data.category_id)
#     if not category:
#         raise NotFoundError(f"Category {data.category_id} not found")
#
#     if category.name == data.name:
#         return UpdateResult(modified_count=0)
#
#     return await repository.update_category(
#         category_id=category.id,
#         name=data.name,
#     )
#
#
# async def reorder_skills_categories_command(
#     repository: RepositoryProtocol,
#     /,
#     data: CategoryDisplayOrderUpdate,
# ):
#     pass
#
#

#
#
# async def delete_skills_by_category_command(
#     repository: RepositoryProtocol,
#     /,
#     category_id: EntityId,
# ) -> None:
#     category = await repository.get_category(category_id)
#     if not category:
#         raise NotFoundError(f"Category {category_id} not found")
#
#     await repository.delete_skills_by_category(category_id=category_id)
#     await repository.delete_category(category=category)
