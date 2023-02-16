from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "role_name" VARCHAR(5) NOT NULL,
    "is_seller" BOOL NOT NULL  DEFAULT False,
    "jwt_key" VARCHAR(255),
    "btc_balance" DOUBLE PRECISION,
    "btc_address" VARCHAR(255),
    "otp" VARCHAR(255),
    "city" VARCHAR(255),
    "avatar" VARCHAR(255),
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_banned" BOOL NOT NULL  DEFAULT False,
    "user_ban_date" TIMESTAMPTZ
);
COMMENT ON COLUMN "user"."role_name" IS 'USER: user\nADMIN: admin';
CREATE TABLE IF NOT EXISTS "countries" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS "idx_countries_name_0b12f2" ON "countries" ("name");
CREATE TABLE IF NOT EXISTS "city" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "country_id" INT NOT NULL REFERENCES "countries" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_city_name_468230" ON "city" ("name");
CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS "idx_category_name_8b0cb9" ON "category" ("name");
CREATE TABLE IF NOT EXISTS "subcategory" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_subcategory_name_b6b28e" ON "subcategory" ("name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
