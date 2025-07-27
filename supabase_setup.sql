-- ========================================
-- CRYPTO AI BOT - SUPABASE SETUP
-- ========================================
-- 
-- INSTRUCCIONES:
-- 1. Ejecuta estas consultas en el SQL Editor de Supabase
-- 2. Ejecuta las consultas en el orden indicado
-- 3. Verifica que todas las tablas se creen correctamente

-- ========================================
-- 1. HABILITAR EXTENSIONES NECESARIAS
-- ========================================

-- Habilitar UUID para IDs únicos
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Habilitar pgcrypto para encriptación
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ========================================
-- 2. TABLA DE USUARIOS DE TELEGRAM
-- ========================================

CREATE TABLE IF NOT EXISTS telegram_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_admin BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    preferences JSONB DEFAULT '{}'::jsonb
);

-- Índices para telegram_users
CREATE INDEX IF NOT EXISTS idx_telegram_users_telegram_id ON telegram_users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_telegram_users_username ON telegram_users(username);
CREATE INDEX IF NOT EXISTS idx_telegram_users_is_active ON telegram_users(is_active);

-- ========================================
-- 3. TABLA DE SUGERENCIAS
-- ========================================

CREATE TABLE IF NOT EXISTS suggestions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT NOT NULL,
    suggestion_text TEXT NOT NULL,
    user_info JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    admin_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para suggestions
CREATE INDEX IF NOT EXISTS idx_suggestions_user_id ON suggestions(user_id);
CREATE INDEX IF NOT EXISTS idx_suggestions_status ON suggestions(status);
CREATE INDEX IF NOT EXISTS idx_suggestions_created_at ON suggestions(created_at);

-- ========================================
-- 4. TABLA DE ALERTAS
-- ========================================

CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    condition_type VARCHAR(50) NOT NULL,
    condition_value DECIMAL(20, 8) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    triggered_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para alerts
CREATE INDEX IF NOT EXISTS idx_alerts_user_id ON alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_alerts_symbol ON alerts(symbol);
CREATE INDEX IF NOT EXISTS idx_alerts_is_active ON alerts(is_active);
CREATE INDEX IF NOT EXISTS idx_alerts_condition_type ON alerts(condition_type);

-- ========================================
-- 5. TABLA DE CONFIGURACIONES DE USUARIO
-- ========================================

CREATE TABLE IF NOT EXISTS user_configurations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT UNIQUE NOT NULL,
    preferred_cryptos TEXT[] DEFAULT '{}',
    preferred_timeframes TEXT[] DEFAULT '{}',
    notification_settings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para user_configurations
CREATE INDEX IF NOT EXISTS idx_user_configurations_user_id ON user_configurations(user_id);

-- ========================================
-- 6. TABLA DE LOGS DE ACTIVIDAD
-- ========================================

CREATE TABLE IF NOT EXISTS activity_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT,
    action VARCHAR(100) NOT NULL,
    details JSONB DEFAULT '{}'::jsonb,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para activity_logs
CREATE INDEX IF NOT EXISTS idx_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_action ON activity_logs(action);
CREATE INDEX IF NOT EXISTS idx_activity_logs_created_at ON activity_logs(created_at);

-- ========================================
-- 7. TABLA DE ANÁLISIS TÉCNICOS
-- ========================================

CREATE TABLE IF NOT EXISTS technical_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    analysis_type VARCHAR(50) NOT NULL,
    analysis_data JSONB NOT NULL,
    confidence_score DECIMAL(3, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para technical_analyses
CREATE INDEX IF NOT EXISTS idx_technical_analyses_user_id ON technical_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_technical_analyses_symbol ON technical_analyses(symbol);
CREATE INDEX IF NOT EXISTS idx_technical_analyses_created_at ON technical_analyses(created_at);

-- ========================================
-- 8. TABLA DE SEÑALES DE TRADING
-- ========================================

CREATE TABLE IF NOT EXISTS trading_signals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    signal_type VARCHAR(20) NOT NULL CHECK (signal_type IN ('BUY', 'SELL', 'NEUTRAL')),
    entry_price DECIMAL(20, 8),
    stop_loss DECIMAL(20, 8),
    take_profit DECIMAL(20, 8),
    confidence_score DECIMAL(3, 2),
    reasoning TEXT,
    strategy_used VARCHAR(100),
    is_executed BOOLEAN DEFAULT false,
    executed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para trading_signals
CREATE INDEX IF NOT EXISTS idx_trading_signals_user_id ON trading_signals(user_id);
CREATE INDEX IF NOT EXISTS idx_trading_signals_symbol ON trading_signals(symbol);
CREATE INDEX IF NOT EXISTS idx_trading_signals_signal_type ON trading_signals(signal_type);
CREATE INDEX IF NOT EXISTS idx_trading_signals_created_at ON trading_signals(created_at);

-- ========================================
-- 9. FUNCIONES DE ACTUALIZACIÓN AUTOMÁTICA
-- ========================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para actualizar updated_at
CREATE TRIGGER update_telegram_users_updated_at BEFORE UPDATE ON telegram_users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_suggestions_updated_at BEFORE UPDATE ON suggestions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_alerts_updated_at BEFORE UPDATE ON alerts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_configurations_updated_at BEFORE UPDATE ON user_configurations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- 10. POLÍTICAS RLS (ROW LEVEL SECURITY)
-- ========================================

-- Habilitar RLS en todas las tablas
ALTER TABLE telegram_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE suggestions ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_configurations ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE technical_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE trading_signals ENABLE ROW LEVEL SECURITY;

-- Política para telegram_users (usuarios solo pueden ver sus propios datos)
CREATE POLICY "Users can view own data" ON telegram_users
    FOR SELECT USING (telegram_id = current_setting('app.current_user_id', true)::bigint);

CREATE POLICY "Users can update own data" ON telegram_users
    FOR UPDATE USING (telegram_id = current_setting('app.current_user_id', true)::bigint);

-- Política para suggestions (usuarios pueden crear y ver sus propias sugerencias)
CREATE POLICY "Users can create suggestions" ON suggestions
    FOR INSERT WITH CHECK (user_id = current_setting('app.current_user_id', true)::bigint);

CREATE POLICY "Users can view own suggestions" ON suggestions
    FOR SELECT USING (user_id = current_setting('app.current_user_id', true)::bigint);

-- Política para alerts (usuarios pueden gestionar sus propias alertas)
CREATE POLICY "Users can manage own alerts" ON alerts
    FOR ALL USING (user_id = current_setting('app.current_user_id', true)::bigint);

-- Política para user_configurations (usuarios solo pueden gestionar sus propias configuraciones)
CREATE POLICY "Users can manage own configurations" ON user_configurations
    FOR ALL USING (user_id = current_setting('app.current_user_id', true)::bigint);

-- Política para activity_logs (usuarios solo pueden ver sus propios logs)
CREATE POLICY "Users can view own logs" ON activity_logs
    FOR SELECT USING (user_id = current_setting('app.current_user_id', true)::bigint);

-- Política para technical_analyses (usuarios solo pueden ver sus propios análisis)
CREATE POLICY "Users can view own analyses" ON technical_analyses
    FOR SELECT USING (user_id = current_setting('app.current_user_id', true)::bigint);

-- Política para trading_signals (usuarios solo pueden ver sus propias señales)
CREATE POLICY "Users can view own signals" ON trading_signals
    FOR SELECT USING (user_id = current_setting('app.current_user_id', true)::bigint);

-- ========================================
-- 11. DATOS INICIALES (OPCIONAL)
-- ========================================

-- Insertar usuario admin de ejemplo (cambiar el telegram_id por el tuyo)
-- INSERT INTO telegram_users (telegram_id, username, first_name, last_name, is_admin) 
-- VALUES (123456789, 'admin', 'Admin', 'User', true)
-- ON CONFLICT (telegram_id) DO NOTHING;

-- ========================================
-- 12. VISTAS ÚTILES
-- ========================================

-- Vista para estadísticas de sugerencias
CREATE OR REPLACE VIEW suggestions_stats AS
SELECT 
    status,
    COUNT(*) as count,
    ROUND(AVG(LENGTH(suggestion_text)), 2) as avg_length
FROM suggestions 
GROUP BY status;

-- Vista para estadísticas de usuarios activos
CREATE OR REPLACE VIEW active_users_stats AS
SELECT 
    COUNT(*) as total_users,
    COUNT(CASE WHEN is_admin THEN 1 END) as admin_users,
    COUNT(CASE WHEN last_activity > NOW() - INTERVAL '7 days' THEN 1 END) as active_last_7_days
FROM telegram_users 
WHERE is_active = true;

-- ========================================
-- VERIFICACIÓN FINAL
-- ========================================

-- Verificar que todas las tablas se crearon correctamente
SELECT 
    table_name,
    table_type
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
    'telegram_users',
    'suggestions', 
    'alerts',
    'user_configurations',
    'activity_logs',
    'technical_analyses',
    'trading_signals'
)
ORDER BY table_name; 