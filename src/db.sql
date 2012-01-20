CREATE SEQUENCE document_id_seq;
CREATE TABLE document (
    id INT NOT NULL default nextval('document_id_seq'),
    url VARCHAR(1024) not null,
    PRIMARY KEY(id)
);
CREATE UNIQUE INDEX document_url ON document(url);

CREATE SEQUENCE click_id_seq;
CREATE TABLE click (
    id INT NOT NULL default nextval('click_id_seq'),
    member VARCHAR(255) NOT NULL,
    count INT NOT NULL,
    lastaccess TIMESTAMP NOT NULL,
    document INT REFERENCES document(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(id)
);
CREATE UNIQUE INDEX member_document ON click(member, document);


CREATE OR REPLACE FUNCTION logclick(
    VARCHAR(255), VARCHAR(1024)) RETURNS BOOLEAN AS '
DECLARE
    p_member ALIAS FOR $1;
    p_url ALIAS FOR $2;
    doc RECORD;
BEGIN
    SELECT id INTO doc FROM document WHERE url = p_url;
    IF NOT FOUND THEN
        INSERT INTO document (url) VALUES (p_url) RETURNING id INTO doc;
    END IF;
    UPDATE click SET count = count+1, lastaccess=NOW()
        WHERE member = p_member AND document = doc.id;
    IF NOT FOUND THEN
        INSERT INTO click (member, count, lastaccess, document) VALUES (
            p_member, 1, NOW(), doc.id);
    END IF;
    RETURN FOUND;
END
' LANGUAGE plpgsql;
