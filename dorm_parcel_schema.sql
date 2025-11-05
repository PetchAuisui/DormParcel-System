-- 📦 Dorm Parcel System (Multi-Dorm Edition)

CREATE SCHEMA IF NOT EXISTS dorm_parcel;

SET search_path TO dorm_parcel;

-- 🏢 หอพัก (Dormitories)

CREATE TABLE dormitories (
    dorm_id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    address TEXT,
    building_code VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(20),
    total_floors INT DEFAULT 1,
    total_rooms INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 🚪 ห้องพัก (Rooms)

CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    dorm_id INT REFERENCES dormitories (dorm_id) ON DELETE CASCADE,
    room_number VARCHAR(20) NOT NULL,
    floor INT,
    type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'AVAILABLE',
    UNIQUE (dorm_id, room_number)
);

-- 👤 ผู้ใช้งาน (Users)

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    dorm_id INT REFERENCES dormitories (dorm_id) ON DELETE SET NULL,
    room_id INT REFERENCES rooms (room_id) ON DELETE SET NULL,
    full_name VARCHAR(120) NOT NULL,
    national_id CHAR(13) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    gender VARCHAR(10) CHECK (
        gender IN ('MALE', 'FEMALE', 'OTHER')
    ),
    date_of_birth DATE,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (
        role IN (
            'ADMIN',
            'OWNER',
            'STAFF',
            'OFFICER',
            'RESIDENT'
        )
    ),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 🧩 ความสัมพันธ์ผู้ใช้กับหอ (User-Dorm Roles)

CREATE TABLE user_dorm_roles (
    user_id INT REFERENCES users (user_id) ON DELETE CASCADE,
    dorm_id INT REFERENCES dormitories (dorm_id) ON DELETE CASCADE,
    role_in_dorm VARCHAR(20) NOT NULL CHECK (
        role_in_dorm IN (
            'OWNER',
            'STAFF',
            'OFFICER',
            'RESIDENT'
        )
    ),
    assigned_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (
        user_id,
        dorm_id,
        role_in_dorm
    )
);

-- 🚚 บริษัทขนส่ง (Carriers)

CREATE TABLE carriers (
    carrier_id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 📦 พัสดุ (Parcels)

CREATE TABLE parcels (
    parcel_id SERIAL PRIMARY KEY,
    dorm_id INT REFERENCES dormitories (dorm_id) ON DELETE CASCADE,
    receiver_id INT REFERENCES users (user_id) ON DELETE SET NULL,
    carrier_id INT REFERENCES carriers (carrier_id) ON DELETE SET NULL,
    tracking_code VARCHAR(100) UNIQUE NOT NULL,
    sender_name VARCHAR(120),
    sender_phone VARCHAR(20),
    parcel_image_url TEXT,
    size VARCHAR(50),
    storage_bin VARCHAR(40),
    note TEXT,
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
    received_by INT REFERENCES users (user_id) ON DELETE SET NULL, -- ผู้รับของเข้าระบบ
    received_at TIMESTAMP,
    picked_up_at TIMESTAMP,
    updated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 👥 พนักงานจัดการพัสดุ (Parcel Handlers)

CREATE TABLE parcel_handlers (
    parcel_id INT REFERENCES parcels (parcel_id) ON DELETE CASCADE,
    handler_id INT REFERENCES users (user_id) ON DELETE CASCADE,
    role_in_process VARCHAR(30), -- เช่น STAFF, OFFICER
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (parcel_id, handler_id)
);

-- 🕓 ประวัติการเปลี่ยนสถานะ (Parcel Status History)

CREATE TABLE parcel_status_history (
    history_id SERIAL PRIMARY KEY,
    parcel_id INT REFERENCES parcels (parcel_id) ON DELETE CASCADE,
    changed_by INT REFERENCES users (user_id) ON DELETE SET NULL,
    from_status VARCHAR(20),
    to_status VARCHAR(20),
    remark TEXT,
    changed_at TIMESTAMP DEFAULT NOW()
);

-- 🔐 โค้ดยืนยันรับพัสดุ (Pickup Codes)

CREATE TABLE pickup_codes (
    code_id SERIAL PRIMARY KEY,
    parcel_id INT UNIQUE REFERENCES parcels (parcel_id) ON DELETE CASCADE,
    code_hash TEXT NOT NULL,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 🔔 การแจ้งเตือน (Notifications)

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

-- 🧾 บันทึกการทำงาน (Audit Logs)
CREATE TABLE audit_logs (
    audit_id SERIAL PRIMARY KEY,
    actor_user_id INT REFERENCES users (user_id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    target_type VARCHAR(50),
    target_id INT,
    meta JSON,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ✅ ข้อมูลตั้งต้น (Default Data)
INSERT INTO
    carriers (name, code, phone)
VALUES (
        'Thailand Post',
        'THP',
        '1545'
    ),
    (
        'Kerry Express',
        'KEX',
        '1217'
    ),
    (
        'Flash Express',
        'FLE',
        '1436'
    ),
    ('J&T Express', 'JNT', '1470');