from fastapi import HTTPException, status

from src.database.repositories.products import ProductsRepository
from src.schemas.products import ProductDto, ProductResponse


class ProductsService:
    @staticmethod
    async def create(product_dto: ProductDto) -> ProductResponse:
        exists_product = await ProductsRepository.check_exists_product_by_title(product_dto.title)
        if exists_product:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Product already exist')
        product = await ProductsRepository.add(product_dto)
        return product

    @staticmethod
    async def get_product(product_id: int) -> ProductResponse:
        product = await ProductsRepository.get(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
        return product

    @staticmethod
    async def get_products() -> list[ProductResponse]:
        products = await ProductsRepository.get_all()
        if not products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No products found')
        return products

    @staticmethod
    async def edit(product_id: int, new_quantity: int, new_price: int) -> ProductResponse:
        exists_product = await ProductsRepository.check_exists_product_by_id(product_id)
        if not exists_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
        product = await ProductsRepository.edit(product_id=product_id, new_quantity=new_quantity, new_price=new_price)
        return product

    @staticmethod
    async def delete(product_id: int) -> ProductResponse:
        exists_product = await ProductsRepository.check_exists_product_by_id(product_id)
        if not exists_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
        product = await ProductsRepository.delete(product_id)
        return product

    @staticmethod
    async def get_brands() -> list[str]:
        brands = await ProductsRepository.get_brands()
        if not brands:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Brands not found')
        return brands
