
const prod = {
    url: {
        API_URL: '/api',
        BASE_URL: '/',
        IMG_URL: '/',
    }
}

const dev = {
    url: {
        API_URL: 'http://localhost:8000/admin/api',
        BASE_URL: 'http://localhost:8000',
        IMG_URL: 'http://localhost:8000/',
    }
}

const debug = import.meta.env.MODE === 'development'

export const config = debug ? dev : prod
export default config