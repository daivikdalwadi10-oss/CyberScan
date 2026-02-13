import { AuthProvider, useAuth } from "../context/AuthContext.jsx";
import { ThemeProvider } from "../theme/ThemeProvider.jsx";
import { SocketProvider } from "../context/SocketProvider.jsx";


function InnerProviders({ children }) {
  const { token, user } = useAuth();
  return (
    <SocketProvider token={token} role={user?.roles?.[0] || "PublicVisitor"}>
      {children}
    </SocketProvider>
  );
}

export default function Providers({ children }) {
  return (
    <ThemeProvider>
      <AuthProvider>
        <InnerProviders>{children}</InnerProviders>
      </AuthProvider>
    </ThemeProvider>
  );
}
