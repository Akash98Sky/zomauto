import React from 'react';
import { RestaurantItem, RestaurantSearchQuery } from '../models/interfaces';
import { Text, makeStyles, Title2, Caption1, Card, CardHeader, CardPreview, tokens } from '@fluentui/react-components';
import { useQueryRestaurantsByItemQuery } from '../store/reducers/zomautoApi';

interface RestaurantDisplayProps {
    query: RestaurantSearchQuery;
}

const flex = {
    gap: "16px",
    display: "flex",
};

const useStyles = makeStyles({
    main: {
        ...flex,
        flexWrap: "wrap",
        justifyContent: "left",
        overflowX: "hidden",
    },

    row: {
        ...flex,
        width: "95vw",

        overflowX: "scroll",
    },

    card: {
        minWidth: "300px",
        // maxWidth: "100%",
        height: "fit-content",
    },

    section: {
        display: "flex",
        flexDirection: "column",
        textAlign: "left"
    },

    caption: {
        color: tokens.colorNeutralForeground3,
    },

    smallRadius: { borderRadius: tokens.borderRadiusSmall },

    grayBackground: {
        backgroundColor: tokens.colorNeutralBackground3,
    },

    logoBadge: {
        padding: "5px",
        borderRadius: tokens.borderRadiusSmall,
        backgroundColor: "#FFF",
        boxShadow:
            "0px 1px 2px rgba(0, 0, 0, 0.14), 0px 0px 2px rgba(0, 0, 0, 0.12)",
    },
});

export default function RestaurantDisplay(props: RestaurantDisplayProps) {
    const styles = useStyles();
    const { isLoading, isError, data: restaurants } = useQueryRestaurantsByItemQuery(props.query);

    return (
        <div>
            <h1>Restaurant Display</h1>
            {isLoading && <p>Loading...</p>}
            {isError && <p>Failed to load!</p>}
            <ul className={styles.main}>
                {restaurants && restaurants.map(({ restaurant, items, offers }) => (
                    <li key={restaurant.name}>
                        <section className={styles.section}>
                            <Title2>{restaurant.name}</Title2>
                            <p>{restaurant.type}</p>

                            <div className={styles.row}>
                                {items.reduce<RestaurantItem[]>((acc, item) => [...acc, ...item.items] as RestaurantItem[], []).map((item, idx) => (
                                    <Card key={idx} className={styles.card}>
                                        <CardPreview
                                            className={styles.grayBackground}
                                        >
                                            <img
                                                className={styles.smallRadius}
                                                src={item.img}
                                                alt={item.name}
                                            />
                                        </CardPreview>

                                        <CardHeader
                                            header={<Text weight="semibold">{item.name} @ ₹{item.discounted_price}</Text>}
                                            description={
                                                <Caption1 className={styles.caption} strikethrough>₹{item.price}</Caption1>
                                            }
                                        />
                                    </Card>
                                ))}
                            </div>
                        </section>
                    </li>
                ))}
            </ul>
        </div>
    );
}