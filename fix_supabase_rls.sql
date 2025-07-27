-- Script para arreglar las políticas RLS de Supabase
-- Ejecuta este script en el SQL Editor de Supabase

-- 1. Deshabilitar RLS temporalmente para permitir inserción de sugerencias
ALTER TABLE suggestions DISABLE ROW LEVEL SECURITY;

-- 2. Crear una política más permisiva para sugerencias
-- Permitir inserción de sugerencias desde cualquier usuario
CREATE POLICY "Allow suggestion creation" ON suggestions
    FOR INSERT 
    WITH CHECK (true);

-- Permitir lectura de sugerencias para admins (por ahora permitimos todo)
CREATE POLICY "Allow suggestion reading" ON suggestions
    FOR SELECT 
    USING (true);

-- Permitir actualización de sugerencias para admins
CREATE POLICY "Allow suggestion update" ON suggestions
    FOR UPDATE 
    USING (true);

-- 3. Crear políticas para telegram_users
-- Permitir inserción/actualización de usuarios
CREATE POLICY "Allow user creation" ON telegram_users
    FOR INSERT 
    WITH CHECK (true);

CREATE POLICY "Allow user update" ON telegram_users
    FOR UPDATE 
    USING (true);

-- Permitir lectura de usuarios
CREATE POLICY "Allow user reading" ON telegram_users
    FOR SELECT 
    USING (true);

-- 4. Crear políticas para activity_logs
CREATE POLICY "Allow activity logging" ON activity_logs
    FOR INSERT 
    WITH CHECK (true);

CREATE POLICY "Allow activity reading" ON activity_logs
    FOR SELECT 
    USING (true);

-- 5. Crear políticas para alerts
CREATE POLICY "Allow alert creation" ON alerts
    FOR INSERT 
    WITH CHECK (true);

CREATE POLICY "Allow alert reading" ON alerts
    FOR SELECT 
    USING (true);

CREATE POLICY "Allow alert update" ON alerts
    FOR UPDATE 
    USING (true);

CREATE POLICY "Allow alert deletion" ON alerts
    FOR DELETE 
    USING (true);

-- 6. Crear políticas para user_configurations
CREATE POLICY "Allow config creation" ON user_configurations
    FOR INSERT 
    WITH CHECK (true);

CREATE POLICY "Allow config reading" ON user_configurations
    FOR SELECT 
    USING (true);

CREATE POLICY "Allow config update" ON user_configurations
    FOR UPDATE 
    USING (true);

-- 7. Crear políticas para technical_analyses
CREATE POLICY "Allow analysis creation" ON technical_analyses
    FOR INSERT 
    WITH CHECK (true);

CREATE POLICY "Allow analysis reading" ON technical_analyses
    FOR SELECT 
    USING (true);

-- 8. Crear políticas para trading_signals
CREATE POLICY "Allow signal creation" ON trading_signals
    FOR INSERT 
    WITH CHECK (true);

CREATE POLICY "Allow signal reading" ON trading_signals
    FOR SELECT 
    USING (true);

-- 9. Verificar que las políticas se crearon correctamente
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- 10. Probar inserción de una sugerencia de prueba
INSERT INTO suggestions (user_id, suggestion_text, user_info, status)
VALUES (999999, 'Prueba de política RLS', '{"test": true}', 'pending')
ON CONFLICT DO NOTHING;

-- Verificar que se insertó correctamente
SELECT * FROM suggestions WHERE user_id = 999999;

-- Limpiar la sugerencia de prueba
DELETE FROM suggestions WHERE user_id = 999999; 