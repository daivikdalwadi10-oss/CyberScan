import { createContext, useCallback, useContext, useMemo, useState } from "react";
import { ROLE_PERMISSIONS } from "../utils/permissions.js";

const AuthContext = createContext(null);

const storageKeys = {
  accessToken: "access_token",
  refreshToken: "refresh_token",
  role: "role",
  tenantId: "tenant_id",
  user: "user"
};

const getStoredValue = (key, fallback = "") => {
  if (typeof window === "undefined") return fallback;
  return window.localStorage.getItem(key) || fallback;
};

const getStoredJson = (key, fallback = null) => {
  if (typeof window === "undefined") return fallback;
  const raw = window.localStorage.getItem(key);
  if (!raw) return fallback;
  try {
    return JSON.parse(raw);
  } catch (error) {
    return fallback;
  }
};

const getRoleFromUser = (user) => {
  if (!user) return "";
  if (Array.isArray(user.roles) && user.roles.length > 0) {
    return user.roles[0];
  }
  return user.role || "";
};

export const AuthProvider = ({ children }) => {
  const storedUser = getStoredJson(storageKeys.user);
  const storedRole = getStoredValue(storageKeys.role) || getRoleFromUser(storedUser);

  const [accessToken, setAccessToken] = useState(getStoredValue(storageKeys.accessToken));
  const [refreshToken, setRefreshToken] = useState(getStoredValue(storageKeys.refreshToken));
  const [role, setRole] = useState(storedRole);
  const [tenantId, setTenantId] = useState(getStoredValue(storageKeys.tenantId));
  const [user, setUser] = useState(storedUser);

  const permissions = useMemo(() => {
    if (!role) return [];
    return ROLE_PERMISSIONS[role] || [];
  }, [role]);

  const setSession = useCallback((payload) => {
    const {
      accessToken: newAccessToken,
      refreshToken: newRefreshToken,
      role: newRole,
      tenantId: newTenantId,
      user: newUser
    } = payload;

    const resolvedRole = newRole || getRoleFromUser(newUser);

    if (newAccessToken) {
      window.localStorage.setItem(storageKeys.accessToken, newAccessToken);
      setAccessToken(newAccessToken);
    }
    if (newRefreshToken) {
      window.localStorage.setItem(storageKeys.refreshToken, newRefreshToken);
      setRefreshToken(newRefreshToken);
    }
    if (resolvedRole) {
      window.localStorage.setItem(storageKeys.role, resolvedRole);
      setRole(resolvedRole);
    }
    if (newTenantId) {
      window.localStorage.setItem(storageKeys.tenantId, String(newTenantId));
      setTenantId(String(newTenantId));
    }
    if (newUser) {
      window.localStorage.setItem(storageKeys.user, JSON.stringify(newUser));
      setUser(newUser);
    }
  }, []);

  const logout = useCallback(() => {
    Object.values(storageKeys).forEach((key) => window.localStorage.removeItem(key));
    setAccessToken("");
    setRefreshToken("");
    setRole("");
    setTenantId("");
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({
      accessToken,
      refreshToken,
      role,
      tenantId,
      user,
      permissions,
      isAuthenticated: Boolean(accessToken),
      setSession,
      logout
    }),
    [accessToken, refreshToken, role, tenantId, user, permissions, setSession, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};
