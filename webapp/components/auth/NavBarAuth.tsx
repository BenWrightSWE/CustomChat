'use client'

import { useRouter } from "next/navigation";
import { useAppearance } from "@/lib/contexts/AppearanceContext";
import { updateAppearanceCookie } from "@/lib/utils/cookies";
import { MoonIcon, SunIcon } from "@radix-ui/react-icons";
import { Button } from "@radix-ui/themes";

export default function NavBarAuth() {

    const router = useRouter();
    const {appearance, setAppearance} = useAppearance();

    const onAppearanceChange = () => {
        setAppearance(appearance === 'light' ? 'dark' : 'light');
        updateAppearanceCookie(appearance === 'light' ? 'dark' : 'light');
    }

    return(
        <nav className={"fixed w-full flex flex-row justify-between items-center border-b bg-background z-50 text-lg " +
                        "font-header h-16 px-4 shadow-md"}>
            <div></div>
            <a className="flex items-center gap-2 mr-6" href="/">
                <img alt="logo" width="34" height="34" src="/cc_logo.png"/>
                <span className="font-semibold text-2xl">Custom Chat</span>
            </a>
            <Button onClick={onAppearanceChange}>{appearance == "light" ? <SunIcon/> : <MoonIcon/>}</Button>
        </nav>
    );
}