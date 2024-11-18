from app import get_db_connection

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela contexts - precisa ser criada primeiro para que outras tabelas possam referenciá-la
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contexts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type VARCHAR(50) NOT NULL,
        description VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabela products
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        category VARCHAR(50),
        price DECIMAL(10, 2),
        brand VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabela slogans (referencia products e contexts)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS slogans (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        text VARCHAR(255) NOT NULL,
        context_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (context_id) REFERENCES contexts(id)
    );
    """)

    # Tabela campaigns (referencia products e contexts)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS campaigns (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        product_id INT,
        start_date DATE,
        end_date DATE,
        context_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (context_id) REFERENCES contexts(id)
    );
    """)

    # Tabela assets (referencia campaigns e products)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        campaign_id INT,
        product_id INT,
        asset_type VARCHAR(50),
        file_path VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    """)

    # Tabela settings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        setting_name VARCHAR(50) NOT NULL,
        value VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

  # Tabela company_profiles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS company_profiles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(255) NOT NULL,
        location_data TEXT,
        brand_tone TEXT,
        target_audience TEXT,
        call_to_action VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)


    conn.commit()
    cursor.close()
    conn.close()
    print("Banco de dados inicializado.")

if __name__ == '__main__':
    init_db()
