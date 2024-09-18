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
import { LocationSearch } from "../../models/interfaces";
import { useLazyGetLocationsByNameQuery } from "../../store/reducers/zomautoApi";

interface SearchLocationProps {
    onChange?: (location: LocationSearch | undefined) => void;
}

export function SearchLocations(props: SearchLocationProps) {
    const [queryTimeout, setQueryTimeout] = useState(setTimeout(() => { }, 0));
    const [locIdx, setLocIdx] = useState<number>();
    const [fetchLocationsByNameQuery, { data: locations }] = useLazyGetLocationsByNameQuery();
    const upateQueryTimeout = (query: string) => {
        clearTimeout(queryTimeout);
        setQueryTimeout(setTimeout(() => {
            fetchLocationsByNameQuery(query);
        }, 2000));
    }

    // render this location list in bullet points
    return <Field label="Search Location" style={{ maxWidth: 400 }}>
        <TagPicker
            onOptionSelect={(_, data) => {
                if (locIdx === parseInt(data.value)) {
                    setLocIdx(undefined);
                    props.onChange && props.onChange(undefined);
                } else {
                    setLocIdx(parseInt(data.value));
                    props.onChange && props.onChange(locations?.[parseInt(data.value)]);
                }
            }}
            selectedOptions={[`${locIdx}`]}
        >
            <TagPickerControl>
                {locIdx !== undefined && (
                    <TagPickerGroup>
                        <Tag
                            key={locIdx}
                            shape="rounded"
                            media={
                                <Avatar aria-hidden name={locations![locIdx].line1} color="colorful" />
                            }
                            value={locIdx.toString()}
                        >
                            {locations![locIdx].line1}
                        </Tag>
                    </TagPickerGroup>
                )}

                <TagPickerInput aria-label="Search Location" onChange={(e) => upateQueryTimeout(e.target.value)} />
            </TagPickerControl>
            <TagPickerList>
                {
                    locations
                        ?.map((loc, idx) => (
                            <TagPickerOption
                                media={
                                    <Avatar
                                        shape="square"
                                        aria-hidden
                                        name={loc.line1}
                                        color="colorful"
                                    />
                                }
                                value={idx.toString()}
                                key={idx}
                            >
                                {loc.line1 + " - " + loc.line2}
                            </TagPickerOption>
                        )).filter((_, idx) => locIdx !== idx)
                }
            </TagPickerList>
        </TagPicker>
    </Field>;
}