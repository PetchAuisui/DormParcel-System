-- =========================================================
-- 📦 Dorm Parcel System (Extended Edition)
-- รองรับหลายหอ เจ้าของ พนักงาน เจ้าหน้าที่ และระบบพัสดุครบวงจร
-- =========================================================

-- ใช้ schema แยก (ถ้าต้องการ)
CREATE SCHEMA IF NOT EXISTS dorm_parcel;

SET search_path TO dorm_parcel;

-- ---------- dormitories ----------
CREATE TABLE dormitories (
    dorm_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(120),
    building_code VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ---------- users ----------
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    dorm_id INT REFERENCES dormitories (dorm_id) ON DELETE SET NULL,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (
        role IN (
            'ADMIN',
            'OFFICER',
            'RESIDENT',
            'OWNER',
            'STAFF'
        )
    ),
    room_number VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ---------- dorm_owners ----------
CREATE TABLE dorm_owners (
    owner_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    dorm_id INT NOT NULL REFERENCES dormitories (dorm_id) ON DELETE CASCADE,
    since TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (owner_id, dorm_id)
);

-- ---------- dorm_staffs ----------
CREATE TABLE dorm_staffs (
    staff_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    dorm_id INT NOT NULL REFERENCES dormitories (dorm_id) ON DELETE CASCADE,
    position VARCHAR(50),
    hired_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (staff_id, dorm_id)
);

-- ---------- officer_dorms ----------
CREATE TABLE officer_dorms (
    officer_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    dorm_id INT NOT NULL REFERENCES dormitories (dorm_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (officer_id, dorm_id)
);

-- ---------- carriers ----------
CREATE TABLE carriers (
    carrier_id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ---------- parcels ----------
CREATE TABLE parcels (
    parcel_id SERIAL PRIMARY KEY,
    dorm_id INT REFERENCES dormitories (dorm_id) ON DELETE CASCADE,
    carrier_id INT REFERENCES carriers (carrier_id) ON DELETE SET NULL,
    receiver_id INT REFERENCES users (user_id) ON DELETE SET NULL,
    tracking_code VARCHAR(80) UNIQUE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (
        status IN (
            'RECEIVED',
            'NOTIFIED',
            'READY',
            'PICKED_UP',
            'RETURNED',
            'LOST'
        )
    ),
    storage_bin VARCHAR(40),
    note TEXT,
    received_at TIMESTAMP,
    picked_up_at TIMESTAMP,
    updated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ---------- parcel_officers ----------
CREATE TABLE parcel_officers (
    parcel_id INT NOT NULL REFERENCES parcels (parcel_id) ON DELETE CASCADE,
    officer_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    role_in_process VARCHAR(30),
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (parcel_id, officer_id)
);

-- ---------- parcel_status_history ----------
CREATE TABLE parcel_status_history (
    history_id SERIAL PRIMARY KEY,
    parcel_id INT REFERENCES parcels (parcel_id) ON DELETE CASCADE,
    changed_by INT REFERENCES users (user_id) ON DELETE SET NULL,
    from_status VARCHAR(20),
    to_status VARCHAR(20),
    remark TEXT,
    changed_at TIMESTAMP DEFAULT NOW()
);

-- ---------- pickup_codes ----------
CREATE TABLE pickup_codes (
    code_id SERIAL PRIMARY KEY,
    parcel_id INT UNIQUE REFERENCES parcels (parcel_id) ON DELETE CASCADE,
    code_hash TEXT NOT NULL,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ---------- notifications ----------
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users (user_id) ON DELETE CASCADE,
    parcel_id INT REFERENCES parcels (parcel_id) ON DELETE CASCADE,
    channel VARCHAR(20) CHECK (
        channel IN ('EMAIL', 'LINE', 'APP')
    ),
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ---------- audit_logs ----------
CREATE TABLE audit_logs (
    audit_id SERIAL PRIMARY KEY,
    actor_user_id INT REFERENCES users (user_id) ON DELETE SET NULL,
    action VARCHAR(40) NOT NULL,
    target_type VARCHAR(40),
    target_id INT,
    meta JSON,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT NOW()
);