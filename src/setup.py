import sys
import mariadb
from config import CONFIG

try:
    connection = mariadb.connect(**CONFIG)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = connection.cursor()

# make necessary tables
try:
    cur.execute("""CREATE TABLE IF NOT EXISTS Image (
    ImageID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Filename VARCHAR(255) NOT NULL,
    Filesize INT UNSIGNED NOT NULL,
    Directory VARCHAR(255) NOT NULL,
    Uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Uploader VARCHAR(63) DEFAULT 'Anonymous',
    Source VARCHAR(255),
    DimX INT UNSIGNED,
    DimY INT UNSIGNED
);""")
except e:
    print(e)
    sys.exit(1)

try:
    cur.execute("""CREATE TABLE IF NOT EXISTS Tag (
    TagID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    TagName VARCHAR(63) NOT NULL
);""")
except e:
    print(e)
    sys.exit(1)

try:
    cur.execute("""CREATE TABLE IF NOT EXISTS Namespace (
    NamespaceID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    NamespaceName VARCHAR(63) NOT NULL
);""")
except e:
    print(e)
    sys.exit(1)

try:
    cur.execute("""CREATE TABLE IF NOT EXISTS ImageTagNamespace (
    ImageID INT UNSIGNED NOT NULL,
    TagID INT UNSIGNED NOT NULL,
    NamespaceID INT UNSIGNED NOT NULL,
    CONSTRAINT fk_image
        FOREIGN KEY (ImageID)     REFERENCES Image     (ImageID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_tag
        FOREIGN KEY (TagID)       REFERENCES Tag       (TagID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_namespace
        FOREIGN KEY (NamespaceID) REFERENCES Namespace (NamespaceID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY (ImageID, TagID, NamespaceID)
);""")
except e:
    print(e)
    sys.exit(1)

cur.close()
connection.close()
