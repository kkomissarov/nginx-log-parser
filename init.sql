CREATE TABLE IF NOT EXISTS nginx_logs(
    id UUID DEFAULT gen_random_uuid(),
    hash CHAR(64) UNIQUE NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    ip INET NOT NULL,
    method TEXT NOT NULL,
    url TEXT NOT NULL,
    response_code SMALLINT NOT NULL,
    response_size INT NOT NULL,
    referer TEXT DEFAULT NULL,
    user_agent TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS nginx_logs_created_idx ON nginx_logs(created);
CREATE INDEX IF NOT EXISTS nginx_logs_ip_idx ON nginx_logs(ip);
CREATE INDEX IF NOT EXISTS nginx_logs_url_idx ON nginx_logs(url);
CREATE INDEX IF NOT EXISTS nginx_logs_user_agent_idx ON nginx_logs(user_agent);