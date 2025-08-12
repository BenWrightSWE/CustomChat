"use client";

import { Button } from "@radix-ui/themes";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/contexts/AuthContext";

export function LogOutButtom() {
  const router = useRouter();
  const { logOut } = useAuth();

  /*
  const logout = async () => {
    await supabase.auth.signOut();
    router.push("/login");
  };*/

  return <Button onClick={async () => await logOut}>Logout</Button>;
}
