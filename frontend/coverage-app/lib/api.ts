
export function postCoverageRequest(data: object) {
    return fetch(`${process.env.NEXT_PUBLIC_LIEN}/api/coverage/`, {
        method: "POST",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then((res) => {
        if (!res.ok) {
            return res.text().then((text) => {
            console.error("Erreur serveur :", text);
            throw new Error("Erreur serveur");
            });
        }

        return res.json(); 
        })
        .then((json) => {
        console.log("Réponse JSON :", json);
        return json;
        })
        .catch((err) => {
        console.error("Erreur attrapée :", err.message);
        throw err;
    });
}

