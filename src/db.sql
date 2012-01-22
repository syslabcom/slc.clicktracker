CREATE SEQUENCE document_id_seq;
CREATE TABLE document (
    id INT NOT NULL default nextval('document_id_seq'),
    path VARCHAR(1024) not null,
    PRIMARY KEY(id)
);
CREATE UNIQUE INDEX document_path ON document(path);

CREATE SEQUENCE click_id_seq;
CREATE TABLE click (
    id INT NOT NULL default nextval('click_id_seq'),
    member VARCHAR(255) NOT NULL,
    count INT NOT NULL,
    lastaccess TIMESTAMP NOT NULL,
    document INT REFERENCES document(id) ON DELETE CASCADE ON UPDATE CASCADE,
    url VARCHAR(1024) not null,
    PRIMARY KEY(id)
);
CREATE UNIQUE INDEX member_document_url ON click(member, document, url);

CREATE OR REPLACE FUNCTION logclick(
    VARCHAR(255), VARCHAR(1024), varchar(1024)) RETURNS BOOLEAN AS '
DECLARE
    p_member ALIAS FOR $1;
    p_path ALIAS FOR $2;
    p_url ALIAS FOR $3;
    doc RECORD;
BEGIN
    SELECT id INTO doc FROM document WHERE path = p_path;
    IF NOT FOUND THEN
        INSERT INTO document (path) VALUES (p_path) RETURNING id INTO doc;
    END IF;
    UPDATE click SET count = count+1, lastaccess=NOW()
        WHERE member = p_member AND document = doc.id AND url = p_url;
    IF NOT FOUND THEN
        INSERT INTO click (member, count, lastaccess, document, url) VALUES (
            p_member, 1, NOW(), doc.id, p_url);
    END IF;
    RETURN FOUND;
END
' LANGUAGE plpgsql;
