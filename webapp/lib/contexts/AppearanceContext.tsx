'use client'

import {createContext, useContext, useEffect, useState} from "react";
import {getAppearanceCookie} from "@/lib/utils/cookies";

interface AppearanceContextType {
    appearance: string;
    setAppearance: (theme: string) => void;
}

const AppearanceContext = createContext<AppearanceContextType | undefined>(undefined);

export function AppearanceProvider({ children }: { children: React.ReactNode }) {
    const [appearance, setAppearance] = useState("light");

    useEffect(() => {
        setAppearance(getAppearanceCookie());
        console.log(getAppearanceCookie());
    }, []);

    return (
        <AppearanceContext.Provider value={{ appearance, setAppearance }}>
            {children}
        </AppearanceContext.Provider>
    );
}

export function useAppearance() {
    const context = useContext(AppearanceContext);
    if (!context) {
        throw new Error('useAppearance must be used within AppearanceProvider');
    }
    return context;
}