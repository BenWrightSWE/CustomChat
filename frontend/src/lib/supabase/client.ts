// partially from Supabase template code

import { createBrowserClient } from "@supabase/ssr";

/*
 * Creates browser client to be able to work with the auth session.
 */
export const supabaseClient =
    createBrowserClient(
        process.env.NEXT_PUBLIC_SUPABASE_URL!,
        process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
        {
            auth: {
                autoRefreshToken: true,
                persistSession: false,
                detectSessionInUrl: true,
                storage: typeof window !== 'undefined' ? window.sessionStorage : undefined,
            }
        });
