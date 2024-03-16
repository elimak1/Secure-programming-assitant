export interface User {
    username: string;
}

export interface NewUser extends User {
    password: string;
    confirmPassword: string;
    email: string;
}