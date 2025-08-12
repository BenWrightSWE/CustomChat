//import { createClient } from '@supabase/supabase-js'
import {createClient} from "@/lib/supabase/client";
import {createBrowserClient} from "@supabase/ssr";

/*

 */
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

const supabase = createBrowserClient(
    supabaseUrl,
    supabaseKey,
    {
        auth: {
            autoRefreshToken: true,
            persistSession: true,
            detectSessionInUrl: true,
            storage: typeof window !== 'undefined' ? window.localStorage : undefined,
        }
    }
);

export default supabase;
