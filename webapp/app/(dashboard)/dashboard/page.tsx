'use client'

import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import NavBar from "@/components/default/NavBar";
import { Theme } from "@radix-ui/themes";
import { useEffect, useState } from "react";
import { getAppearanceCookie } from "../../../lib/utils/cookies";
import { Newsreader, Oswald } from "next/font/google";

/*
const supabase = await createClient();

const { data, error } = await supabase.(auth).getUser();
if (error || !data?.user) {
  redirect("/(auth)/login");
}
*/

export default function ProtectedPage() {

    return (
        <>

        </>
    );
}
