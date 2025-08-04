'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useRouter } from "next/navigation";
import supabase from "@/lib/utils/supabase";
import { User, AuthError } from "@supabase/auth-js";

interface AuthContextType {
    user: User | null;
    loading: boolean

    signUp: (email: string, password: string, metadata?: any) => Promise<{ error: AuthError | null}>
    logIn: (email: string, password: string) => Promise<{error: AuthError | null }>;
    logOut: () => Promise<void>;
    resetPassword: (email: string) => Promise<{ error: AuthError | null }>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode}) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();


    useEffect(() => {
        const getInitialUser = async () => {
            try {
                const { data: { user }, error} = await supabase.auth.getUser();
                if (error) {
                    console.error("Error getting session:", error);
                } else {
                    setUser(user);
                }
            } catch (error) {
                console.error("Error in getInitialSession:", error);
            } finally {
                setLoading(false);
            }
        }

        getInitialUser();

        const { data: { subscription } } = supabase.auth.onAuthStateChange(
            (event, session) => {
                setLoading(false);

                switch (event) {
                    case 'SIGNED_IN':
                        setUser(session?.user ?? null);
                        if(window.location.pathname === '/login'){
                            window.location.href = '/dashboard';
                        }
                        break;
                    case 'TOKEN_REFRESHED':
                    case 'USER_UPDATED':
                        setUser(session?.user ?? null);
                        break;
                    case 'SIGNED_OUT':
                        setUser(null);
                        if(window.location.pathname != '/'){
                            window.location.href = '/';
                        }
                        break;
                }
            }
        );

        return () => {
            subscription.unsubscribe();
        };
    }, [router]);

    const signUp = async (email: string, password: string, metadata = {}) => {
        try {
            setLoading(true);

            const { data, error } = await supabase.auth.signUp({
                email,
                password,
                options: {
                    data: metadata
                }
            });

            if (error) {
                console.error("Sign up error:", error.message);
                return { error };
            }

            return { error: null };
        } catch (error) {
            console.error("Unexpected sign up error:", error);
            return { error: error as AuthError };
        } finally {
            router.push("/auth/sign-up-success");
            setLoading(false);
        }
    };

    const logIn = async (email: string, password: string, metadata = {}) => {
        try {
            setLoading(true);

            const { data, error } = await supabase.auth.signInWithPassword({
                email,
                password,
            });

            if (error) {
                console.error("Login error:", error.message);
                return { error };
            }

            return { error: null };
        } catch (error) {
            console.error("Unexpected log in error:", error);
            return { error: error as AuthError };
        } finally {
            setLoading(false);
        }
    };

    const logOut = async () => {
        try {
            setLoading(true);

            const { error } = await supabase.auth.signOut();

            if (error) {
                console.error("Logout error:", error.message);
                return error;
            }

            return { error: null };
        } catch (error) {
            console.error("Unexpected log out error:", error);
            return { error: error as AuthError };
        } finally {
            setLoading(false);
        }
    };

    const forgotPassword = async (email: string) => {
        setLoading(true);
        try {
            const { error } = await supabase.auth.resetPasswordForEmail(email, {
                redirectTo: 'auth/update-password',
            });

            if (error) {
                console.error("Forgot password error:", error.message);
                return error;
            }

            return { error: null };
        } catch (error) {
            console.error("Unexpected forgot password error:", error);
            return { error: error as AuthError };
        } finally {
            setLoading(false);
        }
    };

    const updatePassword = async (password: string)=> {
        setLoading(true);
        try {
            const { error } = await supabase.auth.updateUser({ password });

            if (error) {
                console.error("Forgot password error:", error.message);
                return error;
            }

            return { error: null };
        } catch (error) {
            console.error("Unexpected password update error:", error);
            return { error: error as AuthError };
        } finally {
            setLoading(false);
        }
    }

    const value = {
        // State
        user,
        loading,

        // Methods
        signUp,
        logIn,
        logOut,
        forgotPassword,
        updatePassword,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context == undefined) {
        throw new Error("useAuth must be used within AuthProvider");
    }
    return context
}