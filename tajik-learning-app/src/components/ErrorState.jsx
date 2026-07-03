export default function ErrorState({ message }) {
  return (
    <div className="mx-auto flex max-w-md flex-col items-center gap-3 p-10 text-center">
      <div className="text-4xl">⚠️</div>
      <p className="text-sm text-gray-500">{message}</p>
    </div>
  );
}
