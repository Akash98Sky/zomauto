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

function fetchData<T>(url: string) {
    const promise = fetch(url)
        .then((res) => res.json())

    return wrapPromise<T>(promise)
}

export default fetchData