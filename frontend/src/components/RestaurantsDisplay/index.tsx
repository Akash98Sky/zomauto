import React, { useState } from "react";
import { Caption1, Card, CardHeader, CardPreview, Title2, Text, tokens, makeStyles } from "@fluentui/react-components";
import { RestaurantDetail, RestaurantFilter, RestaurantItem, SearchFilters } from "../../models/interfaces";
import RestaurantsFilter from "./RestaurantsFilter";

export interface RestaurantsDisplayProps {
    restaurants: RestaurantDetail[]
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

export default function RestaurantsDisplay(props: RestaurantsDisplayProps) {
    const styles = useStyles();
    const [filters, setFilters] = useState<SearchFilters>({restaurant: [], item: []});

    const restaurants = props.restaurants.filter(r => filters.restaurant.every(f => {
        if (f.operator === 'eq') {
            return r.restaurant[f.field] === f.value
        } else if (f.operator === 'gt') {
            return r.restaurant[f.field] > f.value
        } else if (f.operator === 'lt') {
            return r.restaurant[f.field] < f.value
        } else if (f.operator === 'contains') {
            r.restaurant[f.field].toString().toLowerCase().includes(f.value.toString().toLowerCase())
        }
    }));
    const filterItems = (items: RestaurantItem[]) => {
        return items.filter(i => filters.item.every(f => {
            if (f.operator === 'eq') {
                return i[f.field] === f.value;
            } else if (f.operator === 'gt') {
                return i[f.field] && i[f.field]! > f.value;
            } else if (f.operator === 'lt') {
                return i[f.field] && i[f.field]! < f.value;
            } else if (f.operator === 'contains') {
                return i[f.field]?.toString().toLowerCase().includes(f.value.toString().toLowerCase());
            }
        }))
    }

    return (
        <div>
            <RestaurantsFilter filters={filters} onFilterChange={setFilters} />
            <ul className={styles.main}>
                {restaurants.map(({ restaurant, items, offers }) => (
                    <li key={restaurant.name}>
                        <section className={styles.section}>
                            <Title2>{restaurant.name}</Title2>
                            <p>{restaurant.type}</p>

                            <div className={styles.row}>
                                {items.reduce<RestaurantItem[]>((acc, item) => [...acc, ...filterItems(item.items)] as RestaurantItem[], []).map((item, idx) => (
                                    <Card key={idx} className={styles.card}>
                                        <CardPreview
                                            className={styles.grayBackground}
                                        >
                                            <img
                                                className={styles.smallRadius}
                                                src={item.img}
                                                alt={item.name}
                                                loading='lazy'
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