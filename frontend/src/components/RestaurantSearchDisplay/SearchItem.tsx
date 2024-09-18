import React, { useState } from "react";
import {
    Avatar,
    Field,
    Tag,
    TagPicker,
    TagPickerControl,
    TagPickerGroup,
    TagPickerInput,
    TagPickerList,
    TagPickerOption
} from "@fluentui/react-components";
import { ItemSearch } from "../../models/interfaces";
import { useLazyGetItemsByNameQuery } from "../../store/reducers/zomautoApi";

interface SearchItemProps {
    onChange?: (item: ItemSearch | undefined) => void;
}

export function SearchItems(props: SearchItemProps) {
    const [queryTimeout, setQueryTimeout] = useState(setTimeout(() => {}, 0));
    const [itemIdx, setItemIdx] = useState<number>();
    const [fetchItemsByNameQuery, { data: items }] = useLazyGetItemsByNameQuery();
    const upateQueryTimeout = (query: string) => {
        clearTimeout(queryTimeout);
        setQueryTimeout(setTimeout(() => {
            fetchItemsByNameQuery(query);
        }, 2000));
    }

    // render this location list in bullet points
    return <Field label="Search Item" style={{ maxWidth: 400 }}>
        <TagPicker
            onOptionSelect={(_, data) => {
                if (itemIdx === parseInt(data.value)) {
                    setItemIdx(undefined);
                    props.onChange && props.onChange(undefined);
                } else {
                    setItemIdx(parseInt(data.value));
                    props.onChange && props.onChange(items?.[parseInt(data.value)]);
                }
            }}
            selectedOptions={[`${itemIdx}`]}
        >
            <TagPickerControl>
                {itemIdx !== undefined && (
                    <TagPickerGroup>
                        <Tag
                            key={itemIdx}
                            shape="rounded"
                            media={
                                <Avatar aria-hidden name={items![itemIdx].name} color="colorful" />
                            }
                            value={itemIdx.toString()}
                        >
                            {items![itemIdx].name}
                        </Tag>
                    </TagPickerGroup>
                )}

                <TagPickerInput aria-label="Search Item" onChange={(e) => upateQueryTimeout(e.target.value)} />
            </TagPickerControl>
            <TagPickerList>
                {
                    items
                        ?.map((item, idx) => (
                            <TagPickerOption
                                media={
                                    <Avatar
                                        shape="square"
                                        aria-hidden
                                        name={item.name}
                                        color="colorful"
                                    />
                                }
                                value={idx.toString()}
                                key={idx}
                            >
                                {item.name}
                            </TagPickerOption>
                        )).filter((_, idx) => itemIdx !== idx)
                }
            </TagPickerList>
        </TagPicker>
    </Field>;
}