import React, { useEffect, useState } from "react";
import fetchData, { PromiseResponse } from "../utils/fetchData";
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
import { ItemSearch } from "../models/interfaces";

interface SearchItemProps {
    onChange?: (item: ItemSearch | undefined) => void;
}

export function SearchItems(props: SearchItemProps) {
    const [query, setQuery] = useState('');
    const [data, setData] = useState<PromiseResponse<ItemSearch[]>>();
    const [itemIdx, setItemIdx] = useState<number>();
    const items = data?.read();

    useEffect(() => {
        const getData = setTimeout(() => {
            if (!query) return;
            try {
                setData(fetchData<ItemSearch[]>(`/api/items?q=${query}`));
            } catch (e) {
                console.log(e);
            }
        }, 2000);

        return () => clearTimeout(getData);
    }, [setData, query]);

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

                <TagPickerInput aria-label="Search Item" onChange={(e) => setQuery(e.target.value)} />
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