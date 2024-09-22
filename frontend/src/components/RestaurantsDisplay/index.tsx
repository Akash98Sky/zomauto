import React from "react";
import { Caption1, Card, CardHeader, CardPreview, Title2, Text, tokens, makeStyles, Badge } from "@fluentui/react-components";

import { RestaurantItem, SearchFilters } from "../../models/interfaces";
import RestaurantsFilter from "./RestaurantsFilter";
import { useAppDispatch, useAppSelector } from "../../store";
import { updateFilters } from "../../store/reducers/restaurants";

export interface RestaurantsDisplayProps {
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
        padding: "5px",
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

    restaurantTitle: {
        display: "flex",
        flexDirection: "row",
        alignItems: "center",

        gap: "10px",
    },

    caption: {
        color: tokens.colorNeutralForeground3,
    },

    imgPreview: {
        borderRadius: tokens.borderRadiusSmall,
        maxHeight: "300px",
    },

    cardPreview: {
        backgroundColor: tokens.colorNeutralBackground3,
        position: "relative",
    },

    itemRating: {
        position: "absolute",
        top: "5px",
        left: "5px",
        zIndex: 1,
    },

    logoBadge: {
        padding: "5px",
        borderRadius: tokens.borderRadiusSmall,
        backgroundColor: "#FFF",
        boxShadow:
            "0px 1px 2px rgba(0, 0, 0, 0.14), 0px 0px 2px rgba(0, 0, 0, 0.12)",
    },
});

export default function RestaurantsDisplay(props: RestaurantsDisplayProps) {
    const styles = useStyles();
    const dispatch = useAppDispatch();
    const { restaurants, filters } = useAppSelector(state => ({ restaurants: state.restaurants.filteredRestaurants, filters: state.restaurants.filters }));

    const setFilters = (updatedfilters: SearchFilters) => {
        console.log(updatedfilters);
        dispatch(updateFilters(updatedfilters));
    }

    return (
        <div>
            <RestaurantsFilter filters={filters} onFilterChange={setFilters} />
            <ul className={styles.main}>
                {restaurants.map(({ restaurant, items, offers }) => (
                    <li key={restaurant.name}>
                        <section className={styles.section}>
                            <Title2 className={styles.restaurantTitle}>
                                {restaurant.name}
                                {restaurant.rating &&
                                    <Badge size="large" appearance="filled" color="success">
                                        <strong>{restaurant.rating} ✰</strong>
                                    </Badge>}
                            </Title2>
                            <p>{restaurant.type}</p>

                            <div className={styles.row}>
                                {items.reduce<RestaurantItem[]>((acc, item) => [...acc, ...item.items] as RestaurantItem[], []).map((item, idx) => (
                                    <Card key={idx} className={styles.card}>
                                        <CardPreview
                                            className={styles.cardPreview}
                                        >
                                            <img
                                                className={styles.imgPreview}
                                                src={item.img || 'images/placeholder.webp'}
                                                alt={item.name}
                                                loading='lazy'
                                            />

                                            {item.rating ?
                                                <div className={styles.itemRating}>
                                                    <Badge appearance="filled" color="success">
                                                        {item.rating} ✰
                                                    </Badge>
                                                </div> : null}
                                        </CardPreview>

                                        <CardHeader
                                            header={<Text weight="semibold">{item.name} @ ₹{item.discounted_price}</Text>}
                                            description={
                                                item.discounted_price != item.price ?
                                                    <Caption1 className={styles.caption} strikethrough>₹{item.price}</Caption1> :
                                                    null
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