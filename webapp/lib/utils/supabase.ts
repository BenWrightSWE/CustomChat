import { createClient } from '@supabase/supabase-js'
import { useRouter } from "next/navigation";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseKey)

export const logout = async (router) => {
    const supabase = createClient(supabaseUrl, supabaseKey);
    await supabase.auth.signOut();
    router.push("/");
};