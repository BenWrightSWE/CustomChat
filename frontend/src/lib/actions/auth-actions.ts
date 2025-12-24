"use server"

import { createClient } from "@/lib/supabase/server";
import { revalidatePath } from "next/cache";
import { phoneRegex, emailRegex } from "@/lib/utils/regex";
import { CreateUserParams } from "@/lib/context/auth-context";

/*
    Signs up the user and adds them to the Supabase auth.users table.
 */
export async function signUpAction(userData: CreateUserParams) {
    try {
        const supabase = await createClient();

        if (userData.password !== userData.repeatPassword) {
            return { error: "Passwords don't match." };
        }

        if(userData.phone && userData.phone !== "") {
            if (!phoneRegex.test(userData.phone)) {
                return { error: "Phone number is not formatted in any valid way." };
            } else {
                userData.phone = userData.phone.replace(/\D/g, '');
            }
        }

        // Build options object and include user metadata (options.data) when present.
        const signUpOptions: any = {
            emailRedirectTo: `${process.env.NEXT_PUBLIC_SITE_URL}/verify-email`
        };

        const result = await supabase.auth.signUp({
            email: userData.email,
            password: userData.password,
            options: signUpOptions,
        });

        revalidatePath('create-account', 'layout');

        return result.error ? result.error : null;
    } catch (unexpectedError) {
        return unexpectedError;
    }
}

/*
 * Logs in the user and creates a session for the user
 */
export async function logInAction(email: string, password: string) {
    try {
        const supabase = await createClient();

        const result = await supabase.auth.signInWithPassword({
            email,
            password,
        });

        revalidatePath('/login', 'layout');

        return result.error ? result.error : null;
    } catch (unexpectedError) {
        return unexpectedError;
    }
}

/*
 * Sends the reset password email.
 */
export async function forgotPasswordAction(email: string) {
    if (!emailRegex.test(email)) {
        return { error: "Phone number is not formatted in any valid way." };
    }

    try {
        const supabase = await createClient();

        const result = await supabase.auth.resetPasswordForEmail(email, {
            redirectTo: `${process.env.NEXT_PUBLIC_SITE_URL}/reset-password`,
        });

        return result.error ? result.error : null;
    } catch (unexpectedError) {
        return unexpectedError;
    }
}

/*
 * Updates the user's password based on the given password.
 */
export async function updatePasswordAction(password: string) {
    try {
        const supabase = await createClient();

        const result = await supabase.auth.updateUser({password: password});

        return result.error ? result.error : null;
    } catch (unexpectedError) {
        return unexpectedError;
    }
}

/*
 * checks the server side user session.
 */
export async function checkUserAction() {
    try {
        const supabase = await createClient();
        const { data: { user }, error } = await supabase.auth.getUser();
        if (user) {
            console.log("here is the user", user);
        } else {
            console.log("no user session in server side");
        }
        return error ? error : null;
    } catch (unexpectedError) {
        return unexpectedError;
    }
}

/*
 * checks if the user is verified
 */
export async function checkVerificationAction() {
    const supabase = await createClient()
    const { data: { user }, error } = await supabase.auth.getUser();

    if (error) {
        console.error('Error fetching user:', error.message);
        return null;
    }

    if (user) {
        return !!user.email_confirmed_at;
    } else {
        console.log('no user session in server side');
        return null;
    }
}