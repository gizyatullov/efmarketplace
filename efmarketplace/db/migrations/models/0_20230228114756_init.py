from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
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
CREATE INDEX IF NOT EXISTS "idx_users_usernam_266d85" ON "users" ("username");
COMMENT ON COLUMN "users"."role_name" IS 'USER: user\nADMIN: admin';
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
CREATE TABLE IF NOT EXISTS "categories" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS "idx_categories_name_c47ef4" ON "categories" ("name");
CREATE TABLE IF NOT EXISTS "subcategories" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "category_id" INT NOT NULL REFERENCES "categories" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_subcategori_name_35783d" ON "subcategories" ("name");
CREATE TABLE IF NOT EXISTS "notifications" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "sender" VARCHAR(255) NOT NULL,
    "whom" VARCHAR(255) NOT NULL,
    "text" TEXT NOT NULL,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "notification_statuses" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "status" BOOL NOT NULL  DEFAULT False,
    "notification_id" INT NOT NULL REFERENCES "notifications" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_notificatio_user_id_68eb2c" UNIQUE ("user_id", "notification_id")
);
CREATE TABLE IF NOT EXISTS "tickets" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tag" TEXT NOT NULL,
    "content" TEXT NOT NULL,
    "status" VARCHAR(6) NOT NULL  DEFAULT 'new',
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "sender_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "tickets"."status" IS 'NEW: new\nACTIVE: active\nCLOSED: closed';
COMMENT ON TABLE "tickets" IS 'Ticket model.';
CREATE TABLE IF NOT EXISTS "ticket_responses" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "sender_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "ticket_id" INT NOT NULL REFERENCES "tickets" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "ticket_responses" IS 'Model for response on ticket.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
