
// regular expression for formatted phone numbers
export const phoneRegex = new RegExp("^\\s*(?:\\+?(\\d{1,3}))?[-. (]*(\\d{3})[-. )]*(\\d{3})[-. ]*(\\d{4})\\s*$");

// regular expression for emails - more permissive version
// Accepts most common email formats
export const emailRegex = new RegExp("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$");

// regular expression for passwords 8-20 digits longs. Must have 1 upper, 1 lower, 1 number, 1 special character.
// Gotten off of stack overflow
export const passwordRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[#$@!%&*?])[A-Za-z\\d#$@!%&*?]{8,20}$");

// regular expression for US zip codes
export const zipRegex = new RegExp("^\\b\\d{5}\\b$");

export const specRegex = new RegExp("^.*[#$@!%&*?].*$");

export const upperRegex = new RegExp("^.*[A-Z].*$");

export const lowerRegex = new RegExp("^.*[a-z].*$");

export const numRegex = new RegExp("^.*[0-9].*$");

export const dateRegex = new RegExp("^\\d{4}-\\d{2}-\\d{2}$");

export const isValidDate = (dateString) => {
    if (!dateRegex.test(dateString)) {
        return false;
    }
    const date = new Date(dateString);
    return !isNaN(date.getTime()) && date.toISOString().startsWith(dateString);
};