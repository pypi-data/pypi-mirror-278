import React from "react";
import PropTypes from "prop-types";
import { ArrayField, TextField, GroupField } from "react-invenio-forms";
import { i18next } from "@translations/nr/i18next";
import { LocalVocabularySelectField } from "@js/oarepo_vocabularies";
import { StringArrayField } from "../StringArray/StringArrayField";
import {
  ArrayFieldItem,
  EDTFDaterangePicker,
  sanitizeInput,
} from "@js/oarepo_ui";
import { useFormikContext, getIn } from "formik";

export const EventsField = ({ fieldPath, helpText, validTags }) => {
  const { values, setFieldValue, setFieldTouched } = useFormikContext();

  return (
    <ArrayField
      addButtonLabel={i18next.t("Add event")}
      fieldPath={fieldPath}
      label={i18next.t("Events")}
      labelIcon="pencil"
      helpText={helpText}
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <ArrayFieldItem
            indexPath={indexPath}
            arrayHelpers={arrayHelpers}
            className={"invenio-group-field events"}
            fieldPathPrefix={fieldPathPrefix}
          >
            <TextField
              width={16}
              fieldPath={`${fieldPathPrefix}.eventNameOriginal`}
              label={i18next.t("Event name")}
              required
              placeholder={i18next.t("Write down the main name of the event.")}
              onBlur={() => {
                const cleanedContent = sanitizeInput(
                  getIn(values, `${fieldPathPrefix}.eventNameOriginal`),
                  validTags
                );
                setFieldValue(
                  `${fieldPathPrefix}.eventNameOriginal`,
                  cleanedContent
                );
                setFieldTouched(`${fieldPathPrefix}.eventNameOriginal`, true);
              }}
            />
            <StringArrayField
              width={16}
              fieldPath={`${fieldPathPrefix}.eventNameAlternate`}
              label={i18next.t("Event alternate name")}
              addButtonLabel={i18next.t("Add event alternate name")}
              helpText={i18next.t(
                "If event has other known names, write them here."
              )}
            />
            <EDTFDaterangePicker
              required
              fieldPath={`${fieldPathPrefix}.eventDate`}
              label={i18next.t("Event date")}
            />
            <GroupField>
              <TextField
                width={10}
                fieldPath={`${fieldPathPrefix}.eventLocation.place`}
                label={i18next.t("Place")}
                placeholder={i18next.t("Write down the place of the event.")}
                required
              />
              <LocalVocabularySelectField
                selectOnBlur={false}
                width={6}
                fieldPath={`${fieldPathPrefix}.eventLocation.country`}
                label={
                  <label htmlFor={`${fieldPathPrefix}.eventLocation.country`}>
                    {i18next.t("Country")}
                  </label>
                }
                optionsListName="countries"
                clearable
                placeholder={i18next.t("Choose country from the list.")}
              />
            </GroupField>
          </ArrayFieldItem>
        );
      }}
    </ArrayField>
  );
};

EventsField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};
