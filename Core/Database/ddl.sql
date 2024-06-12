CREATE TABLE
    Dll_Path (
        Tia_Version INTEGER PRIMARY KEY,
        path VARCHAR(200)
    );

CREATE TABLE
    CPU_List (
        mlfb VARCHAR(50) PRIMARY KEY,
        type VARCHAR(50),
        description VARCHAR(500)
    );

SELECT * FROM Dll_Path;

INSERT INTO Dll_Path (Tia_Version, Path) VALUES (17, 'C:\\Program Files\\Siemens\\Automation\\Portal V17\\PublicAPI\\V.17\\Siemens.Engineering.dll')
