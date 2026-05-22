const toTagTitles = (items: Array<{ name?: string }> | null | undefined) => {
  if (!items || !items.length) {
    return []
  }

  return items
    .map((item) => item?.name)
    .filter((name): name is string => Boolean(name))
}

const toEntityOptions = (items: Array<{ id?: number; name?: string }> | null | undefined) => {
  if (!items || !items.length) {
    return []
  }

  return items
    .filter((item) => item?.name)
    .map((item) => ({
      id: item.id ?? null,
      title: item.name,
      isCustom: false,
    }))
}

const toSeriesOption = (id: number | null | undefined, name: string | null | undefined) => {
  if (!name) {
    return ''
  }

  return {
    id: id ?? null,
    title: name,
    isCustom: false,
  }
}

export const useBookFormat = () => {
  const transformBookDataToCards = (bookData: any) => {
    return [
      {
        title: 'Title',
        icon: 'mdi-book-open-page-variant',
        headerColor: 'primary',
        shortText: bookData?.title || 'N/A',
        expandedText: bookData?.original_title || 'N/A',
        expanded: false,
      },
      {
        title: 'Authors',
        icon: 'mdi-account-edit',
        headerColor: 'secondary',
        shortText: bookData?.authors || 'N/A',
        expandedText: bookData?.authors || 'N/A',
        tags: toTagTitles(bookData?.authors_details),
        expanded: false,
      },
      {
        title: 'Publisher',
        icon: 'mdi-domain',
        headerColor: 'info',
        shortText: bookData?.publishers || 'N/A',
        expandedText: bookData?.publishers || 'N/A',
        tags: toTagTitles(bookData?.publishers_details),
        expanded: false,
      },
      {
        title: 'Series',
        icon: 'mdi-book-multiple',
        headerColor: 'teal',
        shortText: bookData?.series_name || 'N/A',
        expandedText: bookData?.series_name || 'N/A',
        expanded: false,
      },
    ]
  }

  const transformBookDataToBigCards = (bookData: any) => {
    return [
      {
        title: 'Description',
        icon: 'mdi-text-box-outline',
        headerColor: 'orange',
        shortText: bookData?.description || 'N/A',
        expandedText: bookData?.description || 'N/A',
        expanded: false,
      },
      {
        title: 'Details',
        icon: 'mdi-information-outline',
        headerColor: 'indigo',
        shortText: `ISBN: ${bookData?.isbn || 'N/A'} | Pages: ${bookData?.pages || 'N/A'} | Year: ${bookData?.release_date || 'N/A'}`,
        expandedText: `First Polish Release: ${bookData?.first_polish_release_date || 'N/A'} | Format: ${bookData?.format || 'N/A'} | Language: ${bookData?.language_name || 'N/A'} | Translator: ${bookData?.translator || 'N/A'} | Size: ${bookData?.size || 'N/A'}`,
        tags: toTagTitles(bookData?.genres_details),
        expanded: false,
      },
      {
        title: 'Notes',
        icon: 'mdi-note-text-outline',
        headerColor: 'pink',
        shortText: bookData?.note || 'N/A',
        expandedText: bookData?.note || 'N/A',
        tags: toTagTitles(bookData?.labels_details),
        expanded: false,
      },
    ]
  }

  const extractBookDataFromFields = (fields: any) => {
    const source = fields?.originalData || {}

    return {
      isbn: source?.isbn ?? null,
      title: source?.title || '',
      publishYear: source?.release_date ?? null,
      firstPublishYear: source?.first_polish_release_date ?? null,
      format: source?.format || 'unknown',
      size: source?.size || 'none',
      pages: source?.pages ?? null,
      description: source?.description || '',
      notes: source?.note || '',
      originalTitle: source?.original_title || '',
      translator: source?.translator || '',
      language: source?.language_name || '',
      author: toEntityOptions(source?.authors_details),
      publisher: toEntityOptions(source?.publishers_details),
      series: toSeriesOption(source?.series_id, source?.series_name),
      genre: toEntityOptions(source?.genres_details),
      label: toEntityOptions(source?.labels_details),
    }
  }

  return {
    transformBookDataToCards,
    transformBookDataToBigCards,
    extractBookDataFromFields,
  }
}
