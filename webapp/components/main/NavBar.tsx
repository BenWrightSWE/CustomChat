'use client'

import { updateAppearanceCookie } from "../../lib/utils/cookies"
import { Button, DropdownMenu } from "@radix-ui/themes";
import { PersonIcon, MoonIcon, SunIcon, HamburgerMenuIcon, Cross1Icon } from "@radix-ui/react-icons";
import { useEffect, useState } from "react";
import { logout, supabase } from "@/lib/utils/supabase";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {useAppearance} from "@/lib/contexts/AppearanceContext";

export default function NavBar() {

    const router = useRouter();

    const [user, setUser] = useState(null);

    const {appearance, setAppearance} = useAppearance();

    useEffect(() => {
        const getUser = async () => {
            const { data: { user } } = await supabase.auth.getUser();
            setUser(user);
        }

        getUser();
    }, [])

    const [isNav, setIsNav] = useState(false);

    const onAppearanceChange = () => {
        setAppearance(appearance === 'light' ? 'dark' : 'light');
        updateAppearanceCookie(appearance === 'light' ? 'dark' : 'light');
    }

    const onNavChange = () => {
        setIsNav(!isNav);
    }

    return (
        <nav className="flex items-center justify-between h-16 px-4 border-b bg-background z-50 text-lg font-header">
                <a className="flex items-center gap-2 mr-6" href="/webapp/public">
                    <img alt="logo" width="34" height="34" src="/cc_logo.png"/>
                    <span className="font-semibold text-2xl">Custom Chat</span>
                </a>

                <div className="hidden lg:flex items-center gap-6">
                    <a className="cursor-pointer font-medium text-muted-foreground" type="button">Overview</a>
                    <a className="cursor-pointer font-medium text-muted-foreground" type="button">Docs</a>
                    <a className="cursor-pointer font-medium text-muted-foreground" type="button">Pricing</a>
                    <a className="cursor-pointer font-medium text-muted-foreground" type="button">About Us</a>
                </div>
                <div className="hidden lg:flex items-center gap-2 ml-auto">
                    <Button onClick={onAppearanceChange}>{appearance == "light" ? <SunIcon/> : <MoonIcon/>}</Button>
                    <DropdownMenu.Root>
                        <DropdownMenu.Trigger>
                            <Button variant={"soft"}><PersonIcon/></Button>
                        </DropdownMenu.Trigger>
                        <DropdownMenu.Content>
                            {user ? (
                                <><DropdownMenu.Item>Dashboard</DropdownMenu.Item>
                                <DropdownMenu.Item>Settings</DropdownMenu.Item>
                                <DropdownMenu.Item onClick={() => logout(router)}>Log Out</DropdownMenu.Item></>
                                ):(
                                <><DropdownMenu.Item><Link href="/auth/login">Log In</Link></DropdownMenu.Item>
                                <DropdownMenu.Item><Link href="/auth/sign-up">Sign up</Link></DropdownMenu.Item></>
                            )}
                        </DropdownMenu.Content>
                    </DropdownMenu.Root>
                </div>

                <div className="lg:hidden ml-auto flex items-center">
                    <Button onClick={onNavChange}>{isNav ? <Cross1Icon/> : <HamburgerMenuIcon/>}</Button>
                </div>

                {isNav ?
                    <div className="absolute top-16 left-0 w-full bg-background shadow-md px-6 py-4 z-40 flex flex-col items-center gap-4 lg:hidden">
                        <a className="text-center cursor-pointer font-medium text-muted-foreground" type="button">Overview</a>
                        <a className="text-center cursor-pointer font-medium text-muted-foreground" type="button">Docs</a>
                        <a className="text-center cursor-pointer font-medium text-muted-foreground" type="button">Pricing</a>
                        <a className="text-center cursor-pointer font-medium text-muted-foreground" type="button">About Us</a>
                        <div className={"flex flex-row items-center gap-3 border-b-2 pl-10 pr-10 mt-2 mb-2"}><PersonIcon/><span className={""}>Profile</span></div>
                        <div className={"flex flex-col w-full gap-5 sm:flex-row justify-center items-center "}>
                            {user ? (
                                <><Button size={"3"} variant={"surface"} className={""}>Dashboard</Button>
                                    <Button size={"3"} variant={"surface"} className={""}>Settings</Button>
                                    <Button size={"3"} variant={"surface"} className={""} onClick={() => logout(router)}>
                                        Log Out</Button>
                                    <Button size={"3"} className={"w-full pl-5 pr-5"} onClick={onAppearanceChange}>{appearance == "light" ? <SunIcon/> : <MoonIcon/>}</Button></>
                            ):(
                                <><Button size={"4"} variant={"surface"} className={""}><Link href="/auth/login">Log In</Link></Button>
                                    <Button size={"4"} variant={"surface"} className={""}><Link href="/auth/sign-up">Sign up</Link></Button>
                                    <Button size={"4"} className={"w-full pl-5 pr-5"} onClick={onAppearanceChange}>{appearance == "light" ? <SunIcon/> : <MoonIcon/>}</Button></>
                            )}
                        </div>
                    </div> : <></>
                }
        </nav>
    );
}