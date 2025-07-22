'use client'

import { Theme } from "@radix-ui/themes";
import { oswald, newsreader } from "@/lib/utils/fonts";
import { useAppearance } from "@/lib/contexts/AppearanceContext"

export default function ThemeWrapper({ children }: { children: React.ReactNode }) {
    const { appearance } = useAppearance();

    return (
        <Theme appearance={appearance} accentColor={"gold"} className={`${oswald.variable} ${newsreader.variable}`}>
            {children}
        </Theme>
    );
}