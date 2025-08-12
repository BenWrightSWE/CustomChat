import type { Metadata } from "next";
import "@/app/globals.css";
import "@radix-ui/themes/styles.css";
import NavBar from "@/components/default/NavBar";
import ThemeWrapper from "@/components/general/ThemeWrapper";
import {AppearanceProvider} from "@/lib/contexts/AppearanceContext";
import supabase from "@/lib/utils/supabase";
import {AuthProvider} from "@/lib/contexts/AuthContext";

const defaultUrl = "http://localhost:3000";

export const metadata: Metadata = {
    metadataBase: new URL(defaultUrl),
    title: "Custom Chat",
    description: "Custom AI chat bots for businesses.",
};

export default function RootLayout({ children, }: Readonly<{
    children: React.ReactNode; }>) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body>
                <AuthProvider>
                    <AppearanceProvider>
                        <ThemeWrapper>
                            <header className={"shrink z-50"}>
                                <NavBar/>
                            </header>
                            <main className={""}>
                                {children}
                            </main>
                            <footer className={""}>
                                {/* <Footer /> */}
                            </footer>
                        </ThemeWrapper>
                    </AppearanceProvider>
                </AuthProvider>
            </body>
        </html>
    );
}