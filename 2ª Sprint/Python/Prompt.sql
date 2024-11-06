use api6sem;

SELECT
    r.Emissao,
    r.Entrega,
    r.MesBase,
    r.AnoExec,
    r.IDFabrica,
    f.MUN AS Fbrica_Municipio,
    r.IDCliente,
    c.MUN AS Cliente_Municipio,
    r.Incoterm,
    r.Veiculo,
    r.pallets,
    r.QtdTransp,
    r.Moeda,
    r.VlrFrete,
    r.Dist
FROM
    rotas r
JOIN fabricas f ON r.IDFabrica = f.IDFabrica
JOIN clientes c ON r.IDCliente = c.IDCliente;

SELECT r.*, f.MUN AS Fbrica_Municipio
FROM rotas r
JOIN fabricas f ON r.IDFabrica = f.IDFabrica;

SELECT r.*, c.MUN AS Cliente_Municipio
FROM rotas r
JOIN clientes c ON r.IDCliente = c.IDCliente;

select * from rotas;

SELECT DISTINCT r.IDFabrica
FROM rotas r
LEFT JOIN fabricas f ON r.IDFabrica = f.IDFabrica
WHERE f.IDFabrica IS NULL;

SELECT DISTINCT r.IDCliente
FROM rotas r
LEFT JOIN clientes c ON r.IDCliente = c.IDCliente
WHERE c.IDCliente IS NULL;

select * from resum;

select count(IDCliente) as total_clientes
from clientes;

ALTER TABLE clientes
ADD PRIMARY KEY (IDCliente);

ALTER TABLE fabricas
ADD PRIMARY KEY (IDFabrica);

ALTER TABLE rotas
MODIFY COLUMN Emissao DATE;

ALTER TABLE rotas ADD COLUMN Emissao_temp DATE;

SET SQL_SAFE_UPDATES = 0;

UPDATE rotas 
SET Emissao_temp = STR_TO_DATE(Emissao, '%d/%m/%Y') 
WHERE Emissao IS NOT NULL;

SELECT Emissao, Emissao_temp FROM rotas LIMIT 10;

CREATE TABLE Resum (
    IDResum INT AUTO_INCREMENT PRIMARY KEY,
    Emissao DATE,
    Entrega DATE,
    MesBase INT,
    AnoExec INT,
    IDFabrica INT,
    IDCliente INT,
    Incoterm VARCHAR(50),
    Veiculo VARCHAR(50),
    Pallets INT,
    QtdTransp INT,
    Moeda VARCHAR(10),
    VlrFrete DECIMAL(10, 2),
    Dist DECIMAL(10, 2),
    MunFabrica VARCHAR(255),
    LatFabrica FLOAT,
    LongFabrica FLOAT,
    MunCliente VARCHAR(255),
    LatCliente FLOAT,
    LongCliente FLOAT
);

INSERT INTO Resum (Emissao, Entrega, MesBase, AnoExec, IDFabrica, IDCliente, Incoterm, Veiculo, Pallets, QtdTransp, Moeda, VlrFrete, Dist, MunFabrica, LatFabrica, LongFabrica, MunCliente, LatCliente, LongCliente)
SELECT 
    STR_TO_DATE(r.Emissao, '%d/%m/%Y') AS Emissao,
    STR_TO_DATE(r.Entrega, '%d/%m/%Y') AS Entrega,
    r.MesBase,
    r.AnoExec,
    r.IDFabrica,
    r.IDCliente,
    r.Incoterm,
    r.Veiculo,
    r.Pallets,
    r.QtdTransp,
    r.Moeda,
    r.VlrFrete,
    r.Dist,
    f.MUN AS MunFabrica,
    CAST(NULLIF(f.LAT, '') AS DECIMAL(10, 6)) AS LatFabrica,
    CAST(NULLIF(f.LONG, '') AS DECIMAL(10, 6)) AS LongFabrica,
    c.MUN AS MunCliente,
    CAST(NULLIF(c.LAT, '') AS DECIMAL(10, 6)) AS LatCliente,
    CAST(NULLIF(c.LONG, '') AS DECIMAL(10, 6)) AS LongCliente
FROM rotas r
LEFT JOIN fabricas f ON r.IDFabrica = f.IDFabrica
LEFT JOIN clientes c ON r.IDCliente = c.IDCliente;

ALTER TABLE rotas
ADD CONSTRAINT fk_rotas_fabricas
FOREIGN KEY (IDFabrica) REFERENCES fabricas(IDFabrica)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE rotas
ADD CONSTRAINT fk_rotas_clientes
FOREIGN KEY (IDCliente) REFERENCES clientes(IDCliente)
ON DELETE CASCADE
ON UPDATE CASCADE;

SELECT 
    r.Emissao,
    r.Entrega,
    r.MesBase,
    r.AnoExec,
    f.MUN AS MunFabrica,
    f.LAT AS LatFabrica,
    f.LONG AS LongFabrica,
    c.MUN AS MunCliente,
    c.LAT AS LatCliente,
    c.LONG AS LongCliente
FROM rotas r
LEFT JOIN fabricas f ON r.IDFabrica = f.IDFabrica
LEFT JOIN clientes c ON r.IDCliente = c.IDCliente;

SELECT * FROM rotas
ORDER BY Emissao DESC
LIMIT 1;

ALTER TABLE rotas ADD COLUMN ID INT AUTO_INCREMENT PRIMARY KEY

SELECT COUNT(*) FROM rotas;