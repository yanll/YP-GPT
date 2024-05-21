import {useEffect} from 'react';
import {useTranslation} from 'react-i18next';
import { useRouter } from 'next/router';

function Login() {
    const {t} = useTranslation();
    const router = useRouter();

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const token = params.get('yuiassotoken') + '';
        if (token && token !== '' && token !== null && token !== undefined) {
            localStorage.setItem("Authorization", token);
            router.push('/');
        }
    }, []);

    return (
        <div className="p-4 md:p-6 overflow-y-auto">
            <div>登录跳转...</div>
        </div>
    );
}

export default Login;
