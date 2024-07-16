export interface PromiseResponse<T> {
    read: () => T
}

function wrapPromise<T>(promise: Promise<T>) {
    let status = 'pending'
    let response: T

    const suspender = promise.then(
        (res) => {
            status = 'success'
            response = res
        },
        (err) => {
            status = 'error'
            response = err
        },
    )
    const read = () => {
        console.log(status, response)
        switch (status) {
            case 'pending':
                throw suspender
            case 'error':
                throw response
            default:
                return response
        }
    }

    return { read } as PromiseResponse<T>
}

function fetchData<T>(url: string, options?: RequestInit) {
    if (process.env.REACT_APP_BACKEND_URL) {
        url = process.env.REACT_APP_BACKEND_URL + url;
    }
    const promise = fetch(url, options)
        .then((res) => res.json())

    return wrapPromise<T>(promise)
}

export function postData<T>(url: string, body?: { [key: string]: any }) {
    if (process.env.REACT_APP_BACKEND_URL) {
        url = process.env.REACT_APP_BACKEND_URL + url;
    }
    const promise = fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
    })
        .then((res) => res.json())

    return wrapPromise<T>(promise)
}

export default fetchData