import type { Metadata } from "next";
import "@/app/globals.css";
import "@radix-ui/themes/styles.css";
import NavBar from "@/components/main/NavBar";
import ThemeWrapper from "@/components/ThemeWrapper";
import {AppearanceProvider} from "@/lib/contexts/AppearanceContext";

const defaultUrl = process.env.VERCEL_URL
    ? `https://${process.env.VERCEL_URL}`
    : "http://localhost:3000";

export const metadata: Metadata = {
    metadataBase: new URL(defaultUrl),
    title: "Custom Chat",
    description: "Custom AI chat bots for businesses.",
};

export default function RootLayout({ children, }: Readonly<{
    children: React.ReactNode;  }>) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body>
                <AppearanceProvider>
                    <ThemeWrapper>
                        <header className={"shrink z-50"}>
                            <NavBar />
                        </header>
                        <main className={""}>
                            {children}
                        </main>
                        <footer className={""}>
                            {/* <Footer /> */}
                        </footer>
                    </ThemeWrapper>
                </AppearanceProvider>
            </body>
        </html>
    );
}