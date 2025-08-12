'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useRouter } from "next/navigation";
import { User, AuthError } from "@supabase/auth-js";
import { signUpAction, logInAction, forgotPasswordAction, updatePasswordAction,checkUserAction } from "@/lib/actions/auth-actions";
import { CreateUserParams } from "@/lib/types";
import supabase from "@/lib/utils/supabase";

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
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();


    useEffect(() => {
        const getInitialUser = async () => {
            setIsLoading(true);

            try {
                const { data: { user }, error} = await supabase.auth.getUser();

                if (error) {
                    console.error("Error getting session:", error);
                } else {
                    setUser(user);
                }
            } catch (unexpectedError) {
                console.error("Unexpected error getting session:", unexpectedError);
            }

            setIsLoading(false);
        }

        getInitialUser();

        const { data: { subscription } } = supabase.auth.onAuthStateChange(
            (event, session) => {
                setIsLoading(false);

                switch (event) {
                    case 'SIGNED_IN':
                        setUser(session?.user ?? null);
                        if(window.location.pathname === '/login'){
                            window.location.href = '/';
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

    const signUp = async (userData: CreateUserParams) => {
        setIsLoading(true);

        const errorMessage = await signUpAction(userData);

        if (errorMessage) {
                console.error("Error during sign-up:", errorMessage);
        } else {
            window.location.href = "/auth/sign-up-success";
        }

        setIsLoading(false);
    };

    const logIn = async (email: string, password: string) => {
        setIsLoading(true);

        const errorMessage = await logInAction(email, password);

        if (errorMessage) {
            console.error("Error during log-in:", errorMessage.message);
        } else {
            window.location.replace("/");
        }

        setIsLoading(false);
    };

    /*
        Note for self: this is ran server side so that Supabase can properly clean up all browser storage and trigger
        all necessary events.
     */
    const logOut = async () => {
        setIsLoading(true);

        try {
            const {error} = await supabase.auth.signOut();

            if (error) {
                console.error("Error during log-out:", error.message);
            }
        } catch (unexpectedError) {
            console.error("Unexpected error during log-out:", unexpectedError);
        }

        setIsLoading(false);
    };

    const forgotPassword = async (email: string) => {
        setIsLoading(true);

        const errorMessage = await forgotPasswordAction(email);

        if (errorMessage) {
            console.error("Error during forgot password:", errorMessage.message);
        }
        setIsLoading(false);
    };

    const updatePassword = async (password: string)=> {
        setIsLoading(true);

        const errorMessage = await updatePasswordAction(password);

        if (errorMessage) {
            console.error("Error during password update", errorMessage.message);
        }
        setIsLoading(false);
    }

    const checkUser = async () => {
        const errorMessage = await checkUserAction();

        if (errorMessage) {
            console.error("Error during check user", errorMessage.message);
        }
    }

    const value = {
        // State
        user,
        isLoading,

        // Methods
        signUp,
        logIn,
        logOut,
        forgotPassword,
        updatePassword,
        checkUser
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
    return context;
}