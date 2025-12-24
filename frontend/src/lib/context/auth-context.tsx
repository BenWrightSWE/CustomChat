'use client';

import {
    createContext,
    useContext,
    useState,
    useEffect,
    ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { AuthError, User } from "@supabase/auth-js";
import {
    signUpAction,
    logInAction,
    forgotPasswordAction,
    updatePasswordAction,
    checkUserAction,
    checkVerificationAction,
} from "@/lib/actions/auth-actions";
import { supabaseClient } from "@/lib/supabase/client";


// User params for a user to sign up
export interface CreateUserParams {
    email: string;
    password: string;
    repeatPassword: string;
    first_name?: string;
    last_name?: string;
    phone?: string;
}

interface AuthContextType {
    user: User | null;
    admin: boolean | null;
    isLoading: boolean;

    signUp: (userData: CreateUserParams) => Promise<string | null>;
    logIn: (email: string, password: string) => Promise<string | null>;
    logOut: () => Promise<AuthError | null>
    forgotPassword: (email: string) => Promise<string | null>;
    updatePassword: (password: string) => Promise<string | null>;
    checkUser: () => Promise<void>;
    checkVerification: () => Promise<boolean | null>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

/*
 * The component that wraps the components that need access to the Auth methods and vars.
 *
 * Should be used in the layout to make use of the properties of separating client and server components.
 */
export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [admin, setAdmin] = useState<boolean | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        // checks for user session on page load.
        const getInitialUser = async () => {
            setIsLoading(true);

            try {
                const {
                    data: { user },
                    error,
                } = await supabaseClient.auth.getUser();

                if (error) {
                    console.error("Error getting session:", error);
                } else {
                    setUser(user);
                }
            } catch (unexpectedError) {
                console.error("Unexpected error getting session:", unexpectedError);
            }

            setIsLoading(false);
        };

        getInitialUser();

        // performs various actions based on the users session condition (signed in or not)
        const {
            data: { subscription },
        } = supabaseClient.auth.onAuthStateChange(async (event, session) => {
            setIsLoading(false);

            switch (event) {
                case "SIGNED_IN":
                    setUser(session?.user ?? null);
                    break;
                case "TOKEN_REFRESHED":
                case "USER_UPDATED":
                    setUser(session?.user ?? null);
                    break;
                case "SIGNED_OUT":
                    setUser(null);
                    setAdmin(null);
                    break;
            }
        });

        return () => {
            subscription.unsubscribe();
        };
    }, [router]);

    /*
     * Callable function from the browser to sign up a user. Calls the signUpAction to be done server side more securely.
     *
     * Uses CreateUserParams for now until different interface is set up.
     * Need to set up an interface for the user data type being passed to signUp action.
     */
    const signUp = async (userData: CreateUserParams) => {
        setIsLoading(true);

        const errorMessage = await signUpAction(userData);

        if (errorMessage) {
            setIsLoading(false);
            return errorMessage.message;
        } else {
            window.location.href = "verify-email";
        }

        setIsLoading(false);
        return null;
    };

    /*
     * Callable function from the browser to log in a user. Calls the logInAction to be done server side more securely.
     */
    const logIn = async (email: string, password: string) => {
        setIsLoading(true);

        const errorMessage = await logInAction(email, password);

        if (errorMessage) {
            setIsLoading(false);
            return errorMessage.message;
        } else {
            // The redirect logic is handled in the onAuthStateChange listener
            const validated = await checkVerification();
            if (validated) {
                window.location.replace("/");
            } else {
                window.location.replace("/verify-email");
            }
        }

        setIsLoading(false);
        return null;
    };

    /*
     * Logs the user out.
     *
     * this is run server side so that Supabase can properly clean up all browser storage and trigger all
     * necessary events.
     */
    const logOut = async () => {
        setIsLoading(true);

        const result = await supabaseClient.auth.signOut();

        setIsLoading(false);

        return result.error ? result.error : null;
    };

    /*
     * Callable function from the browser if a user forgot their password.
     * Calls the forgotPasswordAction to be done server side more securely.
     */
    const forgotPassword = async (email: string) => {
        setIsLoading(true);

        const errorMessage = await forgotPasswordAction(email);

        setIsLoading(false);

        return errorMessage ? errorMessage.message : null;
    };

    /*
     * Callable function from the browser to update a user's password.
     * Calls the updatePasswordAction to be done server side more securely.
     */
    const updatePassword = async (password: string) => {
        setIsLoading(true);

        const errorMessage = await updatePasswordAction(password);

        setIsLoading(false);
        return errorMessage ? errorMessage.message : null;
    };

    // Checks if a user is in session.
    const checkUser = async () => {
        const errorMessage = await checkUserAction();

        if (errorMessage) {
            console.error("Error during check user:", errorMessage);
        }
    };

    // Checks if a user is validated.
    const checkVerification = async () => {
        const result = await checkVerificationAction();

        if (result === null) {
            console.error("Error during check verification");
            return null;
        }
        return result;
    };

    // The callable methods passed to the component from importing.
    const value: AuthContextType = {
        // State
        user,
        admin,
        isLoading,

        // Methods
        signUp,
        logIn,
        logOut,
        forgotPassword,
        updatePassword,
        checkUser,
        checkVerification,
    };

    return <AuthContext.Provider value={value}>{ children }</AuthContext.Provider>;
};

/*
 * Sets up the use of the Auth methods and vars within the component.
 *
 * The component must be within an AuthContext component or an error will be thrown.
 */
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context == undefined) {
        throw new Error("useAuth must be used within AuthProvider");
    }
    return context;
};
